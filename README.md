# SecAlertSeqMining
Set of scripts for simplification of using [SPMF library](http://www.philippe-fournier-viger.com/spmf/) for sequential rule and pattern mining in cybersecurity alerts.

Scripts provide two functions.
* Generate sequential databases in formats required by SPMF. For this purpose there is `src/databases/generate-db.py` script.
    * Databases can be generated from alerts in [IDEA format](https://idea.cesnet.cz) or alerts in csv with parameters order described in `src/databases/alerts/csv.py` module.
    * Because SPMF requires numeric representation of items for majority of algorithms,
    script generates output file with sequences where items are represented as numbers
    and also csv mapping between numeric representation of items and string representation of items. The mapping is saved in the same directory with `.map` suffix.
    * For more information run `python src/databases/generate-db.py -h`.
* Process outputs of SPMF library (files with rules and patterns). For this purpose there is `src/process-outputs.py` script.
    * The main purpose of processing outputs is replacing numeric representation of items with string representation.
    * For more information run `python src/process-outputs.py -h`.


## Example of usage:
(All scripts are written in python 3.6)

**First of all install required packages.**
```bash
$ pip install -r requirements.txt
```

**Generate sequential database.**

``` bash
$ python src/databases/generate_db.py -i alerts.json -o data/db/ --format basic --db-types src src-port
```
`-i alerts.json` Input file with alerts is `alerts.json`.

`-o data/db/` Databases will be saved into `data/db/` directory.

We specify format as `basic` which means, that generated databases will look as described in `src/databases/formats/basic/abstract.py` module.

Db types was specify as `src src-port` which means that databases defined in `src/databases/formats/basic/src.py` and `src/databases/formats/basic/src-port.py` will be generated.

**Run SPMF algorithms.**

Download `spmf.jar` from http://www.philippe-fournier-viger.com/spmf/index.php?link=download.php.

```bash
$ java -jar spmf.jar run RuleGrowth data/db/basic/src-port data/outputs/src-port.RuleGrowth 0.001 0.1
```
Now we run [RuleGrowth algorithm](http://www.philippe-fournier-viger.com/spmf/index.php?link=documentation.php#rulegrowth) for discovering sequential rules. Rules are stored in `data/outputs/src-port.RuleGrowth` file.


**Process rules of SPMF.**
```bash
$ python src/process-outputs.py -d data/db/basic/src-port -o data/outputs/src-port.RuleGrowth
```
Items inside file `data/outputs/src-port.RuleGrowth` are now replaces with string representation from `data/db/basic/src-port.map` file.


## Generate custom database

If you wanna create your own database, create module containing class named `Database` with constructor and two methods.
* `d = Database(output_dir, file_suffix)` Constructor should be abel to take two positional parameters. Output directory (where database should be saved) and database suffix (add this string to output file name).
* `d.read(alert)` Read method will be called for each alert in input file. Alert is instance of one of the classes from `src/databases/alerts/` package (it depends on what input file will be).
* `d.save()` Save method will be called after processing all alerts with read method.

You can extend `AbstractDatabase` from `src/databases/formats/AbstractDatabase.py` to make implementation of some stuff easier for you.

Put the module inside one of `src/databases/formats/` packages or create your own. Then call `generate-db.py` script with `--format` as the package name and `--db-types` as your module name.
