# Java setup

Follow the steps below in order to have different Java versions installed and switch among them.

1. Install the Java version you want.
    ```bash
    sudo apt update
    sudo apt install openjdk-8-jdk  # sudo apt-get install openjdk-11-jdk
    ```

1. Set `JAVA_HOME` environment variable in `/etc/environment`.
    ```bash
    JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"  # JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
    ```

1. Add the following lines to `~/.bashrc`:
    ```bash
    # >>> java >>>
    source /etc/environment
    export PATH=$JAVA_HOME/bin:$PATH
    # <<< java <<<
    ```

1. Reload `~/.bashrc` by running `source ~/.bashrc`.

1. Configure which version is the default to use in the command line by using `update-alternatives`, which manages which symbolic links are used for different commands.  Once you have run it, you can choose the number to use as a default.
    ```bash
    sudo update-alternatives --config <command>
    ```
    where `command` can be `java`, `javac` (compiler), `javadoc` (documentation generator), `jarsigner` (JAR signing tool), and more.

