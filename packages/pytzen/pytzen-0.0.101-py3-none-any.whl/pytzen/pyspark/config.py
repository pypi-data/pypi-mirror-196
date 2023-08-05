from pyspark.sql import SparkSession

class SparkSessionBuilder:
    """
    A class for building a PySpark `SparkSession` with customizable
    configuration options.
    
    Parameters:
    ----------
    app_name : str, optional (default='MyPySparkApp')
        The name of the Spark application.
    master : str, optional (default='local[*]')
        The URL of the cluster manager for the Spark application.
    executor_memory : str, optional (default='1g')
        The amount of memory to be allocated per executor.
    driver_memory : str, optional (default='1g')
        The amount of memory to be allocated to the driver.
    executor_cores : int, optional (default=1)
        The number of cores to be used per executor.
    driver_cores : int, optional (default=1)
        The number of cores to be used by the driver.
    executor_instances : int, optional (default=1)
        The number of executor instances to be used in the cluster.
    serializer : str, optional
        (default='org.apache.spark.serializer.JavaSerializer')
        The serializer to be used to serialize data in the JVM.
    driver_max_result_size : str, optional (default='1g')
        The maximum size in bytes of the results returned to the driver.
    sql_shuffle_partitions : int, optional (default=200)
        The number of partitions to be used when shuffling data in Spark
        SQL.
    sql_catalog_implementation : str, optional (default='hive')
        The implementation of the Spark SQL catalog.
    sql_time_zone : str, optional (default=None)
        The time zone to be used by the Spark SQL session.
    sql_cross_join_enabled : bool, optional (default=False)
        Whether cross-joins are allowed in Spark SQL queries.
    sql_broadcast_join_threshold : str, optional (default='10MB')
        The maximum size in bytes for a table that can be broadcasted in
        a join operation.
    sql_in_memory_batch_size : int, optional (default=10000)
        The batch size for in-memory columnar storage.
    event_log_enabled : bool, optional (default=False)
        Whether event logging is enabled.
    event_log_dir : str, optional (default='file:/tmp/spark-events')
        The directory where event logs are stored.
    executor_java_options : str, optional (default='')
        Extra Java options to be passed to the executor process.
    driver_java_options : str, optional (default='')
        Extra Java options to be passed to the driver process.
    driver_host : str, optional (default='localhost')
        The hostname or IP address of the machine where the driver
        program is running.
    
    Returns:
    -------
    SparkSession
        A PySpark `SparkSession` object with the specified configuration
        options.
    """

    
    def __init__(self, app_name='MyPySparkApp', master='local[*]',
                 executor_memory='1g', driver_memory='1g', executor_cores=1,
                 driver_cores=1, executor_instances=1,
                 serializer='org.apache.spark.serializer.JavaSerializer',
                 driver_max_result_size='1g', sql_shuffle_partitions=200,
                 sql_catalog_implementation='hive',
                 sql_time_zone=None, sql_cross_join_enabled=False,
                 sql_broadcast_join_threshold='10MB',
                 sql_in_memory_batch_size=10000, event_log_enabled=False,
                 event_log_dir='file:/tmp/spark-events',
                 executor_java_options='', driver_java_options='',
                 driver_host='localhost') -> None:
        """
        Initialize a `SparkSessionBuilder` object with the specified
        configuration options.
        """

        self.app_name = app_name
        self.master = master
        self.executor_memory = executor_memory
        self.driver_memory = driver_memory
        self.executor_cores = executor_cores
        self.driver_cores = driver_cores
        self.executor_instances = executor_instances
        self.serializer = serializer
        self.driver_max_result_size = driver_max_result_size
        self.sql_shuffle_partitions = sql_shuffle_partitions
        self.sql_catalog_implementation = sql_catalog_implementation
        self.sql_time_zone = sql_time_zone
        self.sql_cross_join_enabled = sql_cross_join_enabled
        self.sql_broadcast_join_threshold = sql_broadcast_join_threshold
        self.sql_in_memory_batch_size = sql_in_memory_batch_size
        self.event_log_enabled = event_log_enabled
        self.event_log_dir = event_log_dir
        self.executor_java_options = executor_java_options
        self.driver_java_options = driver_java_options
        self.driver_host = driver_host
        

    def build(self) -> SparkSession:
        """
        Build and return a PySpark `SparkSession` object with the
        specified configuration options.

        Returns:
        -------
        SparkSession
            A PySpark `SparkSession` object with the specified
            configuration options.
        """

        spark_builder = (
            SparkSession.builder
            .appName(self.app_name)
            .master(self.master)
            .config("spark.executor.memory", self.executor_memory)
            .config("spark.driver.memory", self.driver_memory)
            .config("spark.executor.cores", str(self.executor_cores))
            .config("spark.driver.cores", str(self.driver_cores))
            .config("spark.executor.instances", str(self.executor_instances))
            .config("spark.serializer", self.serializer)
            .config("spark.driver.maxResultSize", self.driver_max_result_size)
            .config("spark.sql.shuffle.partitions",
                    str(self.sql_shuffle_partitions))
            .config("spark.sql.catalogImplementation",
                    self.sql_catalog_implementation)
            .config("spark.sql.crossJoin.enabled",
                    str(self.sql_cross_join_enabled))
            .config("spark.sql.autoBroadcastJoinThreshold",
                    self.sql_broadcast_join_threshold)
            .config("spark.sql.inMemoryColumnarStorage.batchSize",
                    str(self.sql_in_memory_batch_size))
            .config("spark.eventLog.enabled", str(self.event_log_enabled))
            .config("spark.eventLog.dir", self.event_log_dir)
            .config("spark.executor.extraJavaOptions",
                    self.executor_java_options)
            .config("spark.driver.extraJavaOptions", self.driver_java_options)
            .config("spark.driver.host", self.driver_host)
        )
        if self.sql_time_zone is not None:
            spark_builder.config("spark.sql.session.timeZone",
                                 self.sql_time_zone)
            
        return spark_builder.getOrCreate()