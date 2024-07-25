import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";
import { TAGS } from "../constants";


export const createCertificate = (name: string, certificateOptions: {
  domainName: pulumi.Input<string>,
  validationMethod: string,
  zoneId: pulumi.Input<string>,
  currentRegion?: pulumi.Input<aws.Region>,
  targetRegion?: pulumi.Input<aws.Region>
}): pulumi.Output<string> => {

  const certidficate = new aws.acm.Certificate(`${name}-certificate`, {
    domainName: certificateOptions?.domainName,
    validationMethod: certificateOptions?.validationMethod ?? 'DNS',
    tags: TAGS
  });

  const validationRecord = new aws.route53.Record(`${name}-certificate-record`, {
    zoneId: certificateOptions?.zoneId!,
    name: certidficate.domainValidationOptions[0].resourceRecordName,
    type: certidficate.domainValidationOptions[0].resourceRecordType,
    records: [certidficate.domainValidationOptions[0].resourceRecordValue],
    ttl: 60,
    allowOverwrite: true,
  });

  const validation = new aws.acm.CertificateValidation(`${name}-certificate-validation`, {
    certificateArn: certidficate.arn,
    validationRecordFqdns: [validationRecord.fqdn],
  });

  return validation.certificateArn;
}
