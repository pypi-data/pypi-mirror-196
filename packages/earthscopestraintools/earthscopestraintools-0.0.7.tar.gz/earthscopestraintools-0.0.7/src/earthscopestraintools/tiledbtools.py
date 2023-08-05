import datetime
import tiledb
import numpy as np
import pandas as pd
import json
import logging
from typing import Union

logger = logging.getLogger(__name__)


def str_to_unix_ms(time_string: str):
    # convert string into unix ms
    return np.datetime64(time_string, "ms").astype(int)


class StrainArray:
    def __init__(self, uri: str, period: float = None):
        self.set_default_ctx()
        self.uri = uri
        self.period = period

    def default_config(self):
        # return a tiledb config
        config = tiledb.Config()
        config["vfs.s3.region"] = "us-east-2"
        config["vfs.s3.scheme"] = "https"
        config["vfs.s3.endpoint_override"] = ""
        config["vfs.s3.use_virtual_addressing"] = "true"
        config["sm.consolidation.mode"] = "fragment_meta"
        config["sm.vacuum.mode"] = "fragment_meta"
        return config

    def set_default_ctx(self):
        config = self.default_config()
        self.ctx = tiledb.Ctx(config=config)

    def get_schema_from_s3(self, schema_type):
        s3_schema_uri = f"s3://tiledb-strain/STRAIN_SCHEMA_{schema_type}.tdb"
        logger.info(f"Using schema {s3_schema_uri}")
        config = tiledb.Config()
        config["vfs.s3.region"] = "us-east-2"
        config["vfs.s3.scheme"] = "https"
        config["vfs.s3.endpoint_override"] = ""
        config["vfs.s3.use_virtual_addressing"] = "true"
        config["sm.consolidation.mode"] = "fragment_meta"
        config["sm.vacuum.mode"] = "fragment_meta"

        with tiledb.open(s3_schema_uri, "r", config=config) as A:
            schema = A.schema
        return schema

    def get_schema(self, schema_type):
        filters1 = tiledb.FilterList([tiledb.ZstdFilter(level=7)])
        filters2 = tiledb.FilterList(
            [tiledb.ByteShuffleFilter(), tiledb.ZstdFilter(level=7)]
        )
        filters3 = tiledb.FilterList(
            [tiledb.BitWidthReductionFilter(), tiledb.ZstdFilter(level=7)]
        )
        filters4 = tiledb.FilterList(
            [tiledb.DoubleDeltaFilter(), tiledb.ZstdFilter(level=7)]
        )
        filters5 = tiledb.FilterList(
            [tiledb.FloatScaleFilter(1e-6, 0, bytewidth=8), tiledb.ZstdFilter(level=7)]
        )
        filters6 = tiledb.FilterList(
            [
                tiledb.PositiveDeltaFilter(),
                tiledb.BitWidthReductionFilter(),
                tiledb.ZstdFilter(level=7),
            ]
        )

        if schema_type == "3D":
            ## time dimension with micro-second precision and 24 hour tiles, domain 1970 to 2100
            d0 = tiledb.Dim(name="data_type", dtype="ascii", filters=filters1)
            d1 = tiledb.Dim(name="timeseries", dtype="ascii", filters=filters1)
            d2 = tiledb.Dim(
                name="time",
                domain=(0, 4102444800000),
                tile=86400000,
                dtype=np.int64,
                filters=filters4,
            )

            dom = tiledb.Domain(d0, d1, d2)

            a0 = tiledb.Attr(name="data", dtype=np.float64, filters=filters1)
            a1 = tiledb.Attr(name="quality", dtype="ascii", var=True, filters=filters1)
            a2 = tiledb.Attr(name="level", dtype="ascii", var=True, filters=filters1)
            a3 = tiledb.Attr(name="version", dtype=np.int64, filters=filters1)
            attrs = [a0, a1, a2, a3]

        elif schema_type == "2D_INT":
            ## time dimension with micro-second precision and 24 hour tiles, domain 1970 to 2100
            d0 = tiledb.Dim(name="channel", dtype="ascii", filters=filters1)
            d1 = tiledb.Dim(
                name="time",
                domain=(0, 4102444800000),
                tile=86400000,
                dtype=np.int64,
                filters=filters4,
            )
            dom = tiledb.Domain(d0, d1)

            a0 = tiledb.Attr(name="data", dtype=np.int32, filters=filters4)
            attrs = [a0]

        elif schema_type == "2D_FLOAT":
            ## time dimension with micro-second precision and 24 hour tiles, domain 1970 to 2100
            d0 = tiledb.Dim(name="channel", dtype="ascii", filters=filters1)
            d1 = tiledb.Dim(
                name="time",
                domain=(0, 4102444800000),
                tile=86400000,
                dtype=np.int64,
                filters=filters4,
            )
            dom = tiledb.Domain(d0, d1)

            a0 = tiledb.Attr(name="data", dtype=np.float64, filters=filters1)
            attrs = [a0]

        else:
            raise NameError

        schema = tiledb.ArraySchema(
            domain=dom,
            sparse=True,
            attrs=attrs,
            cell_order="row-major",
            tile_order="row-major",
            capacity=100000,
            offsets_filters=filters6,
        )

        return schema

    def create(self, schema_type: str, schema_source: str = "s3"):
        # schema should be one of 2D_INT, 2D_FLOAT, 3D. case insensitive
        schema_type = schema_type.upper()
        if schema_type in ["2D_INT", "2D_FLOAT", "3D"]:
            if schema_source == "s3":
                self.schema = self.get_schema_from_s3(schema_type)
            else:
                self.schema = self.get_schema(schema_type)
        else:
            logger.error("Invalid schema.  Must be one of 2D_INT, 2D_FLOAT, 3D")
            raise NameError

        try:
            tiledb.Array.create(self.uri, self.schema, ctx=self.ctx)
            logger.info(f"Created array at {self.uri}")
        except tiledb.TileDBError as e:
            logger.warning(e)

    def delete(self):
        try:
            tiledb.remove(self.uri, ctx=self.ctx)
            print("Deleted ", self.uri)
        except tiledb.TileDBError as e:
            print(e)

    def consolidate_fragment_meta(self, print_it=True):
        config = self.ctx.config()
        config["sm.consolidation.mode"] = "fragment_meta"
        tiledb.consolidate(self.uri, config=config)
        if print_it:
            logger.info("consolidated fragment_meta")

    def consolidate_array_meta(self, print_it=True):
        config = self.ctx.config()
        config["sm.consolidation.mode"] = "array_meta"
        tiledb.consolidate(self.uri, config=config)
        if print_it:
            logger.info("consolidated array_meta")

    def consolidate_fragments(self, print_it=True):
        config = self.ctx.config()
        config["sm.consolidation.mode"] = "fragments"
        tiledb.consolidate(self.uri, config=config)
        if print_it:
            logger.info("consolidated fragments")

    def vacuum_fragment_meta(self, print_it=True):
        config = self.ctx.config()
        config["sm.vacuum.mode"] = "fragment_meta"
        tiledb.vacuum(self.uri, config=config)
        if print_it:
            logger.info("vacuumed fragment_meta")

    def vacuum_array_meta(self, print_it=True):
        config = self.ctx.config()
        config["sm.vacuum.mode"] = "array_meta"
        tiledb.vacuum(self.uri, config=config)
        if print_it:
            logger.info("vacuumed array_meta")

    def vacuum_fragments(self, print_it=True):
        config = self.ctx.config()
        config["sm.vacuum.mode"] = "fragments"
        tiledb.vacuum(self.uri, config=config)
        if print_it:
            logger.info("vacuumed fragments")

    def cleanup_meta(self):
        self.consolidate_array_meta(print_it=False)
        self.vacuum_array_meta(print_it=False)
        self.consolidate_fragment_meta(print_it=False)
        self.vacuum_fragment_meta(print_it=False)
        logger.info("Consolidated and vacuumed metadata")

    def cleanup(self):
        self.consolidate_array_meta(print_it=False)
        self.vacuum_array_meta(print_it=False)
        self.consolidate_fragment_meta(print_it=False)
        self.vacuum_fragment_meta(print_it=False)
        self.consolidate_fragments(print_it=False)
        self.vacuum_fragments(print_it=False)
        logger.info("Consolidated and vacuumed fragments and metadata")

    def get_nonempty_domain(self):
        with tiledb.open(self.uri, "r", ctx=self.ctx) as A:
            return A.nonempty_domain()[-1][0], A.nonempty_domain()[-1][1]

    def get_data_types(self):
        with tiledb.open(self.uri, "r", ctx=self.ctx) as A:
            return json.loads(A.meta["dimensions"])["data_types"]

    def get_timeseries(self):
        with tiledb.open(self.uri, "r", ctx=self.ctx) as A:
            return json.loads(A.meta["dimensions"])["timeseries"]

    def get_channels(self):
        with tiledb.open(self.uri, "r", ctx=self.ctx) as A:
            return json.loads(A.meta["channels"])["channels"]

    def print_schema(self):
        with tiledb.open(self.uri, "r", ctx=self.ctx) as A:
            print(A.schema)


class ProcessedStrainReader:
    def __init__(self, uri: str, period=300):
        self.array = StrainArray(uri=uri, period=period)

    def to_df(
        self,
        data_types: Union[list, str],
        timeseries: Union[list, str],
        attrs: Union[list, str],
        start_ts: int = None,
        end_ts: int = None,
        start_str: str = None,
        end_str: str = None,
        start_dt: datetime.datetime = None,
        end_dt: datetime.datetime = None,
        reindex=True,
        print_array_range=False,
    ):
        # generic read function. requires all query parameters, accepts strings or lists
        # reindex handles one or more data_types
        # reindex does not handle more than one timeseries or attr, so should be set to False

        try:
            if not start_ts:
                if start_str:
                    start_ts = str_to_unix_ms(start_str)
                elif start_dt:
                    start_ts = int(
                        start_dt.replace(tzinfo=datetime.timezone.utc).timestamp()
                        * 1000
                    )
                else:
                    logger.error("No start time provided for read")
            if not end_ts:
                if end_str:
                    end_ts = str_to_unix_ms(end_str)
                elif start_dt:
                    end_ts = int(
                        end_dt.replace(tzinfo=datetime.timezone.utc).timestamp() * 1000
                    )
                else:
                    logger.error("No start time provided for read")
            logger.info(f"Query range {start_ts} to {end_ts}")
            with tiledb.open(self.array.uri, "r", ctx=self.array.ctx) as A:
                if print_array_range:
                    print(
                        "Array date range: %s to %s"
                        % (A.nonempty_domain()[2][0], A.nonempty_domain()[2][1])
                    )
                index_col = ["data_type", "timeseries", "time"]
                data_types = [data_types] if isinstance(data_types, str) else data_types
                timeseries = [timeseries] if isinstance(timeseries, str) else timeseries
                attrs = [attrs] if isinstance(attrs, str) else attrs
                df = A.query(index_col=index_col, attrs=attrs).df[
                    data_types, timeseries, start_ts:end_ts
                ]
                df.index = df.index.set_levels(
                    pd.to_datetime(df.index.levels[2], unit="ms"), level=2
                )
            if reindex:
                df = self.reindex_df(df, columns=data_types, attr=attrs[0])
            if not isinstance(df, pd.DataFrame):
                df = df.to_frame()
            self.check_query_result(df, start_ts, end_ts)
            return df

        except (IndexError, KeyError) as e:  # tiledb.TileDBError
            logger.error(e)
            logger.error("No data found matching query parameters")
            return pd.DataFrame()

    def reindex_df(self, df: pd.DataFrame, columns: list = [], attr="data"):
        # removes a multi-index and makes each data_type a column
        data_types = columns
        for data_type in data_types:
            df_data_type = df.xs(data_type, level="data_type")[attr].droplevel(level=0)
            df_data_type.name = data_type
            if data_type == data_types[0]:
                df2 = df_data_type
            else:
                df2 = pd.concat([df2, df_data_type], axis=1)
        return df2

    def check_query_result(self, df, start, end):
        if self.array.period is not None:
            expected_samples = int((end - start) / 1000 / self.array.period)
            # expected_samples = int((str_to_unix_ms(end) - str_to_unix_ms(start)) / 1000 / self.array.period)
            # print("expected samples:", expected_samples)
            if len(df) >= expected_samples:
                logger.info(
                    f"Query complete, expected {expected_samples} and returned {len(df)}"
                )
            else:
                logger.info(
                    f"Query incomplete, expected {expected_samples} and returned {len(df)}"
                )
        else:
            logger.info(f"Cannot check query completess without array period")


class ProcessedStrainWriter:
    def __init__(self, uri: str):
        self.array = StrainArray(uri=uri)

    def create(self, schema_type: str = "3D", schema_source: str = "s3"):
        self.array.create(schema_type=schema_type, schema_source=schema_source)

    def write_df_to_tiledb(self, df: pd.DataFrame):

        mode = "append"
        tiledb.from_pandas(
            uri=self.array.uri,
            dataframe=df,
            index_dims=["data_type", "timeseries", "time"],
            mode=mode,
            ctx=self.array.ctx,
        )
        # update the string dimension metadata
        data_type = df["data_type"].unique()
        timeseries = df["timeseries"].unique()
        if type(data_type) == str:
            data_type = [data_type]
        if type(timeseries) == str:
            timeseries = [timeseries]
        with tiledb.open(self.array.uri, "r", ctx=self.array.ctx) as A:
            try:
                dimension_json = A.meta["dimensions"]
            except KeyError:
                dimension_json = '{"data_types":[], "timeseries":[]}'

            dimension_dict = json.loads(dimension_json)
            # print(dimension_dict)
            for item in data_type:
                if item not in dimension_dict["data_types"]:
                    dimension_dict["data_types"].append(item)
            for item in timeseries:
                if item not in dimension_dict["timeseries"]:
                    dimension_dict["timeseries"].append(item)

            # print(dimension_dict)
            with tiledb.open(self.array.uri, "w", ctx=self.array.ctx) as A:
                A.meta["dimensions"] = json.dumps(dimension_dict)

    def df_2_tiledb(
        self,
        df: pd.DataFrame,
        data_types: list,
        timeseries: str,
        level: str,
        quality_df: pd.DataFrame = None,
        print_it: bool = False,
    ):
        """
        prepares a dataframe to write to array schema
        df - dataframe with time index, columns are timeseries data (one column per data_type)
        uri - string. which tiledb array to write to
        data_types - list of strings. data_types to map columns into.  ie CH0, 2Ene, pressure, time_index
        timeseries - string. name of timeseries.  counts, microstrain, offset_c, tide_c, atmp_c, atmp, pore, mjd, doy
        level - 2char string.  '0a', '1a', '2a', '2b'
        quality_df- dataframe, optional.  if not included, quality flags will be set to 'g'
        print_it - bool, optional.  show the constructed dataframe as it is being written to tiledb.
        """
        df_buffer = pd.DataFrame(
            columns=[
                "data_type",
                "timeseries",
                "time",
                "data",
                "level",
                "quality",
                "version",
            ]
        )
        if quality_df is None:
            quality_df = pd.DataFrame(index=df.index)
            for ch in data_types:
                quality_df[ch] = "g"
        for ch in data_types:
            data = df[ch].values
            # convert datetimeindex to unix ms
            timestamps = df.index.astype(int) / 10 ** 6
            version = int(datetime.datetime.now().strftime("%Y%j%H%M%S"))
            quality = quality_df[ch].values

            d = {
                "data_type": ch,
                "timeseries": timeseries,
                "time": timestamps,
                "data": data,
                "level": level,
                "quality": quality,
                "version": version,
            }
            ch_df = pd.DataFrame(data=d)
            # ch_df.loc[ch_df['data'] == 999999, 'quality'] = 'm'
            df_buffer = pd.concat([df_buffer, ch_df], axis=0).reset_index(drop=True)
            df_buffer["time"] = df_buffer["time"].astype(np.int64)
            df_buffer["data"] = df_buffer["data"].astype(np.float64)
            df_buffer["version"] = df_buffer["version"].astype(np.int64)

        if print_it:
            print(df_buffer)
        self.write_df_to_tiledb(df_buffer)


class RawStrainReader:
    def __init__(self, uri: str, period=None):
        self.array = StrainArray(uri=uri, period=period)

    def to_df(
        self,
        channels: Union[list, str],
        start_ts: int = None,
        end_ts: int = None,
        start_str: str = None,
        end_str: str = None,
        start_dt: datetime.datetime = None,
        end_dt: datetime.datetime = None,
        print_array_range=True,
    ):
        # generic read function. requires all query parameters, accepts strings or lists
        try:
            if not start_ts:
                if start_str:
                    start_ts = str_to_unix_ms(start_str)
                elif start_dt:
                    start_ts = int(
                        start_dt.replace(tzinfo=datetime.timezone.utc).timestamp()
                        * 1000
                    )
                else:
                    logger.error("No start time provided for read")
            if not end_ts:
                if end_str:
                    end_ts = str_to_unix_ms(end_str)
                elif start_dt:
                    end_ts = int(
                        end_dt.replace(tzinfo=datetime.timezone.utc).timestamp() * 1000
                    )
                else:
                    logger.error("No start time provided for read")
            logger.info(f"Channel query range: {channels}")
            logger.info(f"Time query range: {start_ts} to {end_ts}")
            with tiledb.open(self.array.uri, "r", ctx=self.array.ctx) as A:
                if print_array_range:
                    print(
                        "Array date range: %s to %s"
                        % (A.nonempty_domain()[1][0], A.nonempty_domain()[1][1])
                    )
                index_col = ["channel", "time"]
                channels = [channels] if isinstance(channels, str) else channels
                attrs = ["data"]
                # logger.info("query start")
                df = A.query(index_col=index_col, attrs=attrs).df[
                    channels, start_ts:end_ts
                ]
                # logger.info("query stop")
                df.index = df.index.set_levels(
                    pd.to_datetime(df.index.levels[1], unit="ms"), level=1
                )
            df = self.reindex_df(df, columns=channels, attr="data")
            if not isinstance(df, pd.DataFrame):
                df = df.to_frame()
            self.check_query_result(df, start_ts, end_ts)
            return df

        except (IndexError, KeyError) as e:  # , tiledb.TileDBError
            logger.error(f"{type(e)}: {e}")
            logger.error("No data found matching query parameters")
            return pd.DataFrame()

    def reindex_df(self, df: pd.DataFrame, columns: list = [], attr="data"):
        # removes a multi-index and makes each data_type a column
        channels = columns
        for channel in channels:
            df_channel = df.xs(channel, level="channel")[attr]  # .droplevel(level=0)
            df_channel.name = channel
            if channel == channels[0]:
                df2 = df_channel
            else:
                df2 = pd.concat([df2, df_channel], axis=1)
        return df2

    def check_query_result(self, df, start, end):
        if self.array.period is not None:
            expected_samples = int((end - start) / 1000 / self.array.period)
            # expected_samples = int((str_to_unix_ms(end) - str_to_unix_ms(start)) / 1000 / self.array.period)
            # print("expected samples:", expected_samples)
            if len(df) >= expected_samples:
                logger.info(
                    f"Query complete, expected {expected_samples} and returned {len(df)}"
                )
            else:
                logger.info(
                    f"Query incomplete, expected {expected_samples} and returned {len(df)}"
                )
        else:
            logger.info(f"Cannot check query completess without array period")


class RawStrainWriter:
    def __init__(self, uri: str, array_type="int"):
        self.array = StrainArray(uri=uri)
        self.array_type = array_type

    def create(self, schema_type: str, schema_source: str = "s3"):
        self.array.create(schema_type=schema_type, schema_source=schema_source)

    def write_df_to_tiledb(self, df: pd.DataFrame):
        mode = "append"
        # make sure there arent any nans, replace with 999999 if so
        df = df.replace(np.nan, 999999)
        tiledb.from_pandas(
            uri=self.array.uri,
            dataframe=df,
            index_dims=["channel", "time"],
            mode=mode,
            ctx=self.array.ctx,
        )
        # update the string dimension metadata
        channels = df["channel"].unique()

        if type(channels) == str:
            channels = [channels]

        with tiledb.open(self.array.uri, "r", ctx=self.array.ctx) as A:
            try:
                channels_json = A.meta["channels"]
            except KeyError:
                channels_json = '{"channels":[]}'

            channels_dict = json.loads(channels_json)
            for item in channels:
                if item not in channels_dict["channels"]:
                    channels_dict["channels"].append(item)

            with tiledb.open(self.array.uri, "w", ctx=self.array.ctx) as A:
                A.meta["channels"] = json.dumps(channels_dict)
        logger.info("Write complete")

    def df_2_tiledb(
        self, df: pd.DataFrame, print_it: bool = False,
    ):
        """
        prepares a dataframe to write to array schema
        df - dataframe with time index, columns are timeseries data (one column per channel)
        print_it - bool, optional.  show the constructed dataframe as it is being written to tiledb.
        """
        df_buffer = pd.DataFrame(columns=["channel", "time", "data"])
        for ch in df.columns:
            data = df[ch].values
            # convert datetimeindex to unix ms
            timestamps = df.index.astype(int) / 10 ** 6

            d = {"channel": ch, "time": timestamps, "data": data}
            ch_df = pd.DataFrame(data=d)
            df_buffer = pd.concat([df_buffer, ch_df], axis=0).reset_index(drop=True)
            if self.array_type == "int":
                df_buffer["data"] = df_buffer["data"].astype(np.int32)
            elif self.array_type == "float":
                df_buffer["data"] = df_buffer["data"].astype(np.float64)
            df_buffer["time"] = df_buffer["time"].astype(np.int64)
        if print_it:
            print(df_buffer)
        self.write_df_to_tiledb(df_buffer)
        self.array.cleanup_meta()
