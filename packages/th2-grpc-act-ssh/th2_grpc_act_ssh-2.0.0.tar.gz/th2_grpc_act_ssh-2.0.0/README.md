# th2 gRPC act ssh library (2.0.0)

This project is a gRPC API for act-ssh component

## How to maintain project
1. Make your changes.
2. Up version of Java package in `gradle.properties` file.
3. Up version of Python package in `package_info.json` file.
4. Commit everything.

## Release Notes

### 2.0.0

+ Migrate to book and pages

### 1.1.0

+ Update grpc-common version

### 1.0.0

+ Up major version for common V3 component

### 0.0.5

+ The exit code value can be unknown when the script or command is interrupting by the act. The interrupted flag will be `true` in this case.
