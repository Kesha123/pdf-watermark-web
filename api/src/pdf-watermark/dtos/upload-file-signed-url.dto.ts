import { IsString, IsNotEmpty } from "class-validator";
import { Transform } from "class-transformer";

export default class UploadFileSignedUrlDto {
  @IsString()
  @IsNotEmpty()
  @Transform(({ value }) => value.toString())
  signedUrl: string;
}