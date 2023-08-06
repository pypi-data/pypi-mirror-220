# **Bigeye CLI**
Version: 0.3.40
## Installation

**Setting up your local/build environment**  
Mac with Pyenv

1. Install [brew](https://brew.sh/)
2. Install [pyenv](https://formulae.brew.sh/formula/pyenv)
3. Install python and define a default global:

```text
pyenv install 3.9.13
pyenv global 3.9.13
```

Conda  
Install [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)  
Create environment with python3.9 or greater

```text
conda create -n bigeye_env python=3.9
conda activate bigeye_env
```

Linux  
Most linux distributes include a default python distribution and we recommend using that default.

**Installing Bigeye-CLI**

You can install the Bigeye-CLI from your command line with the following command:

```text
pip3 install bigeye-cli
```

## Configuration

Before using the Bigeye CLI, you will need to configure your Bigeye credentials and workspaces. You can do this in the following ways:

- Configuration Command
- Environment Variables
- Credentials and Configuration Files

### Configuration Command

The quickest way to get started using the Bigeye CLI is to run the `bigeye configure` command. This command will walk you through the options to establish default credentials and configurations for the Bigeye CLI.

```console
$ bigeye configure
```

Using the bigeye configure command, there are two ways to authenticate: basic authentication and browser authentication.

#### Basic Authentication

If you select basic authentication, the CLI will prompt you to enter your Bigeye username and password. This will create a default credential file at ~/.bigeye/credentials. This credential will be used for all CLI commands  
unless an environment variable is explicitly provided.

#### Browser Authentication

Alternatively, you can use browser authentication. Login to your bigeye workspace on a Chrome, Chromium or  
Firefox browser. Run **bigeye configure** and select browser_auth when prompted in the CLI and follow the  
instructions. If you use Chrome profiles, make sure to specify the profile email address you are logged into.

Note: your authentication will only be valid so long as your browser session is active.

### Environment Variables

You can create an environment variable for your workspace credential and configuration files, this is helpful if you would like to store your credential and configuration files some place other than their default locations (~/.bigeye). You can do this by adding the following to your ~/.bashrc or ~/.zshrc file. Please review the format of these files in the below sections.

```shell
export BIGEYE_API_CRED_FILE=/some/path/to/credentials.ini
export BIGEYE_API_CONFIG_FILE=/some/path/to/config.ini
```

### Credentials and Configuration Files

Lastly, if you want to specify the credential per command, you can always pass a -b parameter with the file path for the desired credential. You can pass a -c parameter with the file path for the desired configuration.

_Sample credentials file:_

```ini Text
[DEFAULT]
base_url = "https://app.bigeye.com",
user = "some_user@bigeye.com",
password = "fakepassword1234"
```

_Sample configuration file:_

```ini
[DEFAULT]
workspace_id = 123
```

#### Configuration Options

The configuration files can help to simplify other CLI commands by defining common options in one file. See  
the table below for the complete list of configuration options.

| **Key**                | **Description**                                                                                     | **Type**      | **Example**                            |
| ---------------------- | --------------------------------------------------------------------------------------------------- | ------------- | -------------------------------------- |
| workspace_id           | The id for the workspace [Required]                                                                 | Int           | 123                                    |
| use_default_credential | Whether or not a unique credential is required for this workspace. Default: True                    | Bool          | True                                   |
| bigconfig_input_path   | The path(s) to bigconfig files that are used for the given workspace.                               | List[strings] | path/bigconfig.yml,path2/bigconfig.yml |
| bigconfig_output_path  | The path used to output bigconfig PLAN reports and FIXME files.                                     | String        | output/bigconfig_reports/              |
| bigconfig_strict_mode  | API errors cause an exception if True. (Validation errors still cause an exception). Default: False | Bool          | False                                  |
| bigconfig_auto_approve | Bigconfig applies should be allowed to run without excplit plan approvals. Default: False           | Bool          | False                                  |

The configuration options above can be manually set directly in your config.ini files or you can utilize the below command to set the config values.

```console
$ bigeye configure set <setting_key> <value> [OPTIONAL WORKSPACE]
$ bigeye configure set bigconfig_input_path path/bigconfig.yml,path2/bigconfig -w data-science
```

To view the current value of any specific configuration you can either open the config.ini file or utilize the below command.

```console
$ bigeye configure get <setting_key> [OPTIONAL WORKSPACE]
$ bigeye configure get bigconfig_input_path -w data-science
```

### Multi-Workspace Support

The credential and configuration files are designed to allow Bigeye CLI users to easily switch between their Bigeye workspaces. Each file enforces the idea of a `DEFAULT` section. All subsequent CLI commands will inherit the properties defined in the `DEFAULT`section unless they are directed otherwise. Every command in the Bigeye CLI has the ability to provide a `--workspace` (`-w`) option to override the use of the default workspace.

To setup a non-default workspace, run the following command:

```console
$ bigeye configure -w data-science
```

Or, open up the files and manually edit them based on your setup. Here are some samples. 

_Sample configuration file with multiple workspaces:_

```ini
[DEFAULT]
workspace_id = 123
bigconfig_input_path = absolute_path/bigconfig.yml,absolute_path2/bigconfig.yml
bigconfig_output_path = absolute_path/output/

[workspace data-science]
workspace_id = 234
use_default_credential = True
bigconfig_input_path = absolute_path/ds/bigconfig.yml,absolute_path2/ds/bigconfig.yml

[workspace dev]
workspace_id = 100
use_default_credential = False
bigconfig_auto_approve = True
bigconfig_input_path = absolute_path/bigconfig.yml,absolute_path2/bigconfig.yml
```

_Sample credentials file with multiple workspaces:_

```ini
[DEFAULT]
base_url = "https://app.bigeye.com",
user = "some_user@bigeye.com",
password = "fakepassword1234"

[dev]
base_url = "https://app.bigeye.com",
user = "some_user@bigeye.com",
password = "fakepassword1234"
```

**Note:** Most use cases will only require you to have a single `DEFAULT` credential that all workspaces can utilize. Running the `bigeye configure -w <workspace-name>` command for a non-default workspace will prompt you to inherit the credentials from default or create a new set of credentials. A workspace credential is only required if the `use_default_credential` setting is set to False in the configuration of the corresponding workspace.

# CLI Documentation