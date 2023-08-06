# Documents Utils

## Usage

```
  docker run --rm -p 5000:5000 chanmo/doc-utils
```

## APIs

### Format Convert

use httpie, convert to pdf
```
  http POST -f :5000/convert_to/pdf file@~/demo.docx
```

use httpie, convert to html
```
  http POST -f :5000/convert_to/html file@~/demo.docx
```
