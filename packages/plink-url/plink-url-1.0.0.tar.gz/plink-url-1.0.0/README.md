# plink
Recursive link analyser, written in Python

## Examples
Basic example:
```bash
plink-url https://github.com/Jessicaward/plink
```

Limit analysis to a single domain:
```bash
plink-url https://jessica.im/Blog/ --whitelist https://jessica.im
```

Block multiple domains:
```bash
plink-url https://jessica.im/ --blacklist https://last.fm https://stackoverflow.com
```

Include extra information:
```bash
plink-url https://jessica.im/ --verbose
```

Specify a depth limit:
```bash
plink-url https://jessica.im/ --depth=3
```

Print extra details about the tool and it's usage:
```bash
plink-url https://jessica.im/ --help
```