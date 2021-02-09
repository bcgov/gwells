# Migration tools

## importer-cli

Usage:
```
oc process -f importer.dc.yaml -p NAMESPACE=26e83e-dev | oc apply -f -
```

```bash
oc -n 26e83e-dev create configmap migration-scripts \
--from-file=scripts/
```