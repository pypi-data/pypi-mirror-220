# Create your own tool package

### Prerequisites
Create a new conda environment using python 3.9 or 3.10. Run below command to install PromptFlow dependencies:
```
// Eventually the dependency is prompt-flow package.
pip install promptflow-sdk[builtins]==0.0.99385094 --extra-index-url https://azuremlsdktestpypi.azureedge.net/promptflow/
```
Install Pytest packages for running tests:
```
pip install pytest
pip install pytest-mock
```

### Detailed steps
In this section, we outline the essential steps to create your tool package. Kindly follow the step-by-step instructions below.

* step 1. To rapidly create your own tool package, duplicate the `tool-package-quickstart` folder. Rename the folder [my_tool_package](/tool-package-quickstart/my_tool_package/) to &lt;your-package-name&gt;.

* step 2. Create your tool  
  Implement tool with @tool decorator. There are two ways to write a tool.

  - Option 1 **[Recommended]**: function implementation way, using [my_tool_1.py](my_tool_package/tools/my_tool_1.py) as a reference.
  - Option 2: class implementation way, referring to [my_tool_2.py](my_tool_package/tools/my_tool_2.py) as an example. 


* step 3. Create tool yaml
  
  Please refer to [my_tool_1.yaml](my_tool_package/yamls/my_tool_1.yaml) for guidance.
  
  Alternatively, use the following command under `tool-package-quickstart` folder to generate the tool meta yaml file:
  ```
  python ..\scripts\package_tools_generator.py -m <tool_module> -o <tool_yaml_path>
  ```
  For example:
  ```
  python ..\scripts\package_tools_generator.py -m my_tool_package.tools.my_tool_1 -o my_tool_package\yamls\my_tool_1.yaml
  ```
  In auto gened yaml, tool name is autofilled with tool function name. You may want to update to a better one with description, so that tool can have a great name and description hint in prompt flow UI.

* step 4. Replace `my_tool_package` with &lt;your-package-name&gt; in the [MANIFEST.in](MANIFEST.in) file.

* step 5. Implement list tool API

  In order to make your custom tools can be listed from promptflow UI, make sure put the [utils.py](my_tool_package/tools/utils.py) in the same folder of tools source code, and `yaml_dir` variable in `list_package_tools()` function point to the right path.


* step 6. Configure entry point in package `setup.py`

  In Python, configuring the entry point in [setup.py](setup.py) helps establish the primary execution point for a package, streamlining its integration with other software. The `package_tools` entry point is specifically utilized by the user interface to automatically display your tools.
  
  Replace `PACKAGE_NAME` in [setup.py](setup.py) with your custom package name and configure the entry point:
  ```python
  entry_points={
        "package_tools": ["<your_tool_name> = <list_module>:<list_method>"],
  },
  ```

* step 7. Build and share the tool package

  After configuring the package name, execute the following command in the tool package root directory to build your tool package:
  ```
  python setup.py sdist bdist_wheel
  ```
  This will generate a tool package `<your-package>-0.0.1.tar.gz` and corresponding `whl file` inside the `dist` folder.

  Create an account on PyPI if you don't already have one, and install `twine` package by running `pip install twine`.

  Upload your package to PyPI by running `twine upload dist/*`, this will prompt you for your Pypi username and password, and then upload your package on PyPI. Once your package is uploaded to PyPI, others can install it using pip by running `pip install your-package-name`. Make sure to replace `your-package-name` with the name of your package as it appears on PyPI.

  If you only want to put it on Test PyPI, upload your package by running `twine upload --repository-url https://test.pypi.org/legacy/ dist/*`. Once your package is uploaded to Test PyPI, others can install it using pip by running `pip install --index-url https://test.pypi.org/simple/ your-package-name`.
