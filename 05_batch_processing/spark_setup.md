# Spark setup (Linux)

1. [Install Java](./java_setup.md).
    * According to the [docs](https://spark.apache.org/docs/3.3.3/), since v3.3 Spark runs on Java 8/11/17.

1. [Download Spark](https://archive.apache.org/dist/spark/).
    ```bash
    wget https://archive.apache.org/dist/spark/spark-3.3.3/spark-3.3.3-bin-hadoop3.tgz
    ```

1. Unpack the downloaded file, rename the resulting file as `spark`, and move it to `/opt` directory.
    ```bash
    tar xzfv spark-3.3.3-bin-hadoop3.tgz && rm spark-3.3.3-bin-hadoop3.tgz
    mv spark-3.3.3-bin-hadoop3 spark
    sudo mv spark /opt
    ```

1. In `~/.bashrc`, create a `SPARK_HOME` environment variable and add it to `PATH`.
    ```bash
    export SPARK_HOME=/opt/spark
    export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
    ```

1. Reload `~/.bashrc` by running `source ~/.bashrc`.

1. Check Spark version by running `spark-shell --version`.

1. Test Spark by executing `spark-shell` and running the following:
    ```scala
    val data = 1 to 10000
    val distData = sc.parallelize(data)
    distData.filter(_ < 10).collect()
    ```

1. **PySpark**
    * In `~/.bashrc`, add PySpark to `PYTHONPATH`.
        ```bash
        export PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
        export PYTHONPATH=$SPARK_HOME/python/lib/*.zip:$PYTHONPATH
        ```
    * Reload `~/.bashrc` by running `source ~/.bashrc`.