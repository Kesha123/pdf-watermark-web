import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import { TAGS } from '../constants';

export const createBucket = (name: string, bucketOptions?: {
  forceDestroy?: boolean,
  enableVersioning: boolean,
}) => {
  const bucket = new aws.s3.BucketV2(name, {
    objectLockEnabled: false,
    bucket: name,
    forceDestroy: bucketOptions?.forceDestroy,
    tags: TAGS,
  });

  new aws.s3.BucketPolicy(
    `${name}-policy`,
    {
      bucket: bucket.bucket,
      policy: {
        Version: '2008-10-17',
        Statement: [
          {
            Sid: 'OnlyAllowAccessViaSSL',
            Effect: 'Deny',
            Principal: '*',
            Action: 's3:*',
            Resource: [
              pulumi.interpolate`arn:aws:s3:::${bucket.bucket}`,
              pulumi.interpolate`arn:aws:s3:::${bucket.bucket}/*`,
            ],
            Condition: {
              Bool: {
                'aws:SecureTransport': 'false',
              },
            },
          },
        ],
      },
    },
    { deleteBeforeReplace: true },
  );

  new aws.s3.BucketVersioningV2(`${name}-versioning`, {
    bucket: bucket.id,
    versioningConfiguration: {
      status: 'Enabled',
    },
  });

}
