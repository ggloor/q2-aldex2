# Testing

To test these scripts, make sure that you have `nose` installed.

To install it, run `conda install nose`.

The tests can be run via `nosetests .`

The command line can be run as follows

```
qiime aldex2 aldex2 --i-table data/table.qza --m-metadata-file data/metadata.txt --p-condition labels --output-dir results
```
