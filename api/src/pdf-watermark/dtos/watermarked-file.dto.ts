import { IsString, IsNotEmpty } from 'class-validator';
import { Transform } from 'class-transformer';
import { IsPdfFile } from '../utils/pdf.transformer';

export default class WatermarkedFiledDto {
  @IsString()
  @IsNotEmpty()
  @Transform(({ value }) => value.toString())
  @IsPdfFile()
  pdf_file_s3_bucket_key: string;
}
