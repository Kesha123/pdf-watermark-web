import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import { TAGS } from "../constants";

export const createCloudfrontDistribution = (
  name: string,
  domainName: pulumi.Input<string>,
  certificateArn: pulumi.Input<string>,
  bucketSource: aws.s3.BucketV2,
  acl: aws.wafv2.WebAcl,
) => {

  const originAccessIdentity = new aws.cloudfront.OriginAccessIdentity('originAccessIdentity', {
    comment: 'Access identity for the S3 origin',
  });

  const cachingOptimizedPolicy = aws.cloudfront.getCachePolicy({
    name: 'Managed-CachingOptimized',
  });

  const cachingDisabledPolicy = aws.cloudfront.getCachePolicy({
    name: 'Managed-CachingDisabled',
  });

  const distribution = new aws.cloudfront.Distribution(name, {
    enabled: true,
    isIpv6Enabled: true,
    defaultRootObject: 'index.html',
    priceClass: 'PriceClass_200',
    origins: [
      {
        domainName: bucketSource.bucketRegionalDomainName,
        originId: bucketSource.arn,
        s3OriginConfig: {
          originAccessIdentity: originAccessIdentity.cloudfrontAccessIdentityPath,
        },
      },
    ],
    defaultCacheBehavior: {
      targetOriginId: bucketSource.arn,
      viewerProtocolPolicy: 'redirect-to-https',
      allowedMethods: ['GET', 'HEAD', 'OPTIONS'],
      cachedMethods: ['GET', 'HEAD', 'OPTIONS'],
      cachePolicyId: cachingOptimizedPolicy.then((policy) => policy.id!),
      compress: true,
    },
    orderedCacheBehaviors: [
      {
        pathPattern: '/index.html',
        viewerProtocolPolicy: 'redirect-to-https',
        allowedMethods: ['GET', 'HEAD', 'OPTIONS'],
        cachedMethods: ['GET', 'HEAD', 'OPTIONS'],
        targetOriginId: bucketSource.arn,
        cachePolicyId: cachingDisabledPolicy.then((policy) => policy.id!),
        compress: true,
      },
    ],
    customErrorResponses: [
      {
        errorCode: 403,
        responseCode: 200,
        responsePagePath: '/index.html',
        errorCachingMinTtl: 5,
      },
    ],
    restrictions: {
      geoRestriction: {
        restrictionType: 'none',
      },
    },
    viewerCertificate: {
      acmCertificateArn: certificateArn,
      sslSupportMethod: 'sni-only',
    },
    aliases: [domainName],
    webAclId: acl.arn,
    tags: TAGS,
  });

  new aws.s3.BucketPolicy(`${name}-bucket-policy`, {
    bucket: bucketSource.id,
    policy: {
      Version: '2012-10-17',
      Statement: [
        {
          Effect: 'Allow',
          Principal: {
            AWS: pulumi.interpolate`arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity ${originAccessIdentity.id}`,
          },
          Action: 's3:GetObject',
          Resource: pulumi.interpolate`${bucketSource.arn}/*`,
        },
        {
          Sid: 'OnlyAllowAccessViaSSL',
          Effect: 'Deny',
          Principal: '*',
          Action: 's3:*',
          Resource: [
            pulumi.interpolate`${bucketSource.arn}`,
            pulumi.interpolate`${bucketSource.arn}/*`,
          ],
          Condition: {
            Bool: {
              'aws:SecureTransport': 'false',
            },
          },
        },
      ],
    },
  });

  return distribution;
};
