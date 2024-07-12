import { Transform } from "class-transformer"
import NotPdfFileError from "../errors/not-pdf-file.error"

export const IsPdfFile = () => {
  return Transform(({value}) => {
    if (typeof value === 'string' && !value.endsWith('.pdf')) {
      throw new NotPdfFileError();
    }
    return value;
  })
}