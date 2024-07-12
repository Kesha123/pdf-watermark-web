import { Transform } from 'class-transformer';
import { IsNotEmpty, IsNumber, IsOptional, IsString } from 'class-validator';
import { IsPdfFile } from '../utils/pdf.transformer';

export default class WatermarkCreateInsertDto {
  @IsNumber()
  @IsNotEmpty()
  y: number;

  @IsNumber()
  @IsNotEmpty()
  x: number;

  @IsString()
  @IsNotEmpty()
  @Transform(({ value }) => value.toString())
  horixontal_alignment: string;

  @IsNumber()
  @IsNotEmpty()
  opacity: number;

  @IsNumber()
  @IsNotEmpty()
  angle: number;

  @IsString()
  @IsNotEmpty()
  @Transform(({ value }) => value.toString())
  text_color: string;

  @IsString()
  @IsNotEmpty()
  @Transform(({ value }) => value.toString())
  text_font: string;

  @IsNumber()
  @IsNotEmpty()
  text_size: number;

  @IsNumber()
  @IsNotEmpty()
  image_scale: number;

  @IsNumber()
  @IsNotEmpty()
  dpi: number;

  @IsString()
  @IsNotEmpty()
  @Transform(({ value }) => value.toString())
  @IsPdfFile()
  pdf_file_s3_bucket_key: string;

  @IsString()
  @IsOptional()
  @Transform(({ value }) => value.toString())
  watermark_image_s3_bucket_key: string;

  @IsString()
  @IsOptional()
  @Transform(({ value }) => value.toString())
  watermark_text: string;
}