# minio-keygen

CI/CD Status: ![Main Branch](https://github.com/iandday/minio-keygen/actions/workflows/main.yml/badge.svg) | ![Development Branch](https://github.com/iandday/minio-keygen/actions/workflows/development.yml/badge.svg)

Generate MinIO keys using Python.  This project was created to learn GitHub Actions, Python packaging, and entrypoints.

Example

```code=bash
ian@Ians-MBP minio-keygen % minio-keygen                                   
Key: S9EITflKfJs4pAcOO1o
Secret: vFMzAqChF1PZea_6CMH0vmmcZglziMqDR2zXmtxI
```

## Releasing

```code=bash

   # Set next version number
   export RELEASE=vx.x.x

   # Create tags
   git commit --allow-empty -m "Release $RELEASE"
   git tag -a $RELEASE -m "$RELEASE"

   # Push
   git push --tags
```