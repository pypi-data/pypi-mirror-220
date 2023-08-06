# AWS Secure CloudFront Origin Bucket (for CDK v2)

An AWS CDK construct library to create secure S3 buckets for CloudFront origin.

## Install

### TypeScript

```shell
npm install @gammarer/aws-secure-cloudfront-origin-bucket
# or
yarn add @gammarer/aws-secure-cloudfront-origin-bucket
```

### Python

```shell
pip install gammarer.aws-secure-cloudfront-origin-bucket
```

## Example

### TypeScript

```shell
npm install @gammarer/aws-secure-cloudfront-origin-bucket
```

```python
import { SecureCloudFrontOriginBucket } from '@gammarer/aws-secure-cloudfront-origin-bucket';

const oai = new cloudfront.OriginAccessIdentity(stack, 'OriginAccessIdentity');

new SecureCloudFrontOriginBucket(stack, 'SecureCloudFrontOriginBucket', {
  bucketName: 'example-origin-bucket',
  cloudFrontOriginAccessIdentityS3CanonicalUserId: oai.cloudFrontOriginAccessIdentityS3CanonicalUserId,
});
```

## License

This project is licensed under the Apache-2.0 License.
