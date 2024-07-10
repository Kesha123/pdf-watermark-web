import { Transform } from "class-transformer";
import { IsNotEmpty, IsString } from "class-validator";

export default class UploadFileDto {
  @IsString()
  @IsNotEmpty()
  @Transform(({ value }) => value.toString())
  fileKey: string;
}
