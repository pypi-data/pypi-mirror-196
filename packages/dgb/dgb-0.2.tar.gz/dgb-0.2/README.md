Dynamic Graph Processing
=====
Provides
  1. A data-loader to download a suite of dynamic graph datasets.
  2. An evaluator for the suit of dynamic graph datasets
  3. Tools to benchmark graph models, example code snippets, tutorials, etc. (ongoing...)
----------------------------

## To install

----------------------------
use pip for Python, make sure version python version is 3.6+

```
>>> pip install dgb
```


## Code examples

----------------------------
Code snippet to import the module::
```
import dgb
```
Code snippets to download a dataset::
```   
enron = dgb.TemporalDataSets(data_name="enron")
enron_dict = enron.process()
train = enron_dict["train"]
test  = enron_dict["test"]
val   = enron_dict["validation"]
```

to print all possible datasets::
```
data_list = dgb.list_all()
for data_name in data_list:
print(data_name)
```

to download all possible datasets that have not been downloaded yet::
```
dgb.download_all()
```

to force redownload all datasets::
```
dgb.force_download_all()
```

to skip download prompts and dataset statistics when processing::
```
dgb.TemporalDataSets(data_name="enron", skip_download_prompt=True, data_set_statistics=False)
```

## License

----------------------------
[MIT License](LICENSE)
