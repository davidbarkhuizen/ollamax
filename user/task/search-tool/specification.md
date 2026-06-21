# internet search tool

## inputs

- search_query: str

## processing

- make an asynchronous call to a search engine
  * request text only results, if possible
  * select an appropriate search engine
  * use the input search query
- select only the first result
- make an async call to the URL
- convert the text from the HTML returned to markdown
  * discard all images, styles, videos, audio, etc
- return the markdown document

## outputs

- return the content for thew top search result in markdown format
