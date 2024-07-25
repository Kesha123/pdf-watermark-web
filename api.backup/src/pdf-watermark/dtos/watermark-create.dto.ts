import { Transform } from 'class-transformer';
import { IsEnum, IsNotEmpty, IsNumber, IsOptional, IsString } from 'class-validator';
import { IsPdfFile } from '../utils/pdf.transformer';
import WaterMarkCreateType from '../models/watermark-create-type.enum';

export default class WatermarkCreateDto {
  @IsNumber()
  @IsOptional()
  y: number;

  @IsNumber()
  @IsOptional()
  x: number;

  @IsString()
  @IsOptional()
  @Transform(({ value }) => value.toString())
  horixontal_alignment: string;

  @IsNumber()
  @IsOptional()
  horizontal_boxes: number;

  @IsNumber()
  @IsOptional()
  vertical_boxes: number;

  @IsString()
  @IsOptional()
  @Transform(({ value }) => value.toString())
  margin: string;

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

  @IsString()
  @IsNotEmpty()
  @IsEnum(WaterMarkCreateType)
  watermark_type: WaterMarkCreateType;
}
