# pydantic-settings-yaml

***Note: 2.x needs Pydantic>2.0,<3.0. Install 1.x if you still need Pydantic 1.x.***

Yaml support for Pydantic settings. Load a yaml config file 
as nested Pydantic models. 

Allows to use <file:xxxx> placeholders in the yaml config file
for secrets. A placeholder is replaced with the contents of the
file. Paths are relative to the 'secrets_dir' setting (see below).

## Usage

$cat /config/config.yaml
```
database: 
  password: <file:database_password>
  username: my_database_username
```


$cat /secrets/database_password
```
my_secret_database_password
```


Python code example:
``` 
    from pydantic import BaseModel
    from pydantic_settings_yaml import YamlBaseSettings
    from pydantic_settings import SettingsConfigDict

    class Database(BaseModel):
        username: str
        password: str


    class Settings(YamlBaseSettings):
        database: Database

        # configure paths to secrets directory and YAML config file
        model_config = SettingsConfigDict(
            secrets_dir="/secrets", yaml_file="/config/config.yaml")

    settings = Settings()

    assert settings.dict() == {
        "database": {
            "password": "my_secret_database_password", 
            "username": "my_database_username"
        }
    }
```