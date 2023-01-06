#' @importFrom tblcheck friendly_class
NULL

#' @rdname friendly_class
setMethod("friendly_class", signature("ANY"), function(object) {
  class <- get_friendly_class(object)
  class_str <- knitr::combine_words(md_code(class))
  glue::glue("an object with class {class_str}")
})

setOldClass(c("py_tbl_df", "tbl_df", "tbl", "data.frame"))
#' @rdname friendly_class
setMethod("friendly_class", signature("py_tbl_df"), function(object) {
	if (!setequal(class(object), c("py_tbl_df", "tbl_df", "tbl", "data.frame"))) {
		return(callNextMethod())
	}
	"a DataFrame"
})

setOldClass(c("py_grouped_df", "py_tbl_df", "grouped_df", "tbl_df", "tbl", "data.frame"))
#' @rdname friendly_class
setMethod("friendly_class", signature("py_grouped_df"), function(object) {
	if (!setequal(class(object), c("py_grouped_df", "py_tbl_df", "grouped_df", "tbl_df", "tbl", "data.frame"))) {
		return(callNextMethod())
	}
	"a DataFrame with row labels (i.e. index)"
})

setOldClass(c("int"))
#' @rdname friendly_class
setMethod("friendly_class", signature("int"), function(object) {
  if (!setequal(class(object), "int")) return(callNextMethod())
  "an integer (class `int`)"
})

setOldClass(c("float"))
#' @rdname friendly_class
setMethod("friendly_class", signature("float"), function(object) {
  if (!setequal(class(object), "float")) return(callNextMethod())
  "a floating point number (class `float`)"
})

setOldClass(c("complex"))
#' @rdname friendly_class
setMethod("friendly_class", signature("complex"), function(object) {
  if (!setequal(class(object), "complex")) return(callNextMethod())
  "a complex number (class `complex`)"
})

setOldClass(c("bool"))
#' @rdname friendly_class
setMethod("friendly_class", signature("bool"), function(object) {
  if (!setequal(class(object), "bool")) return(callNextMethod())
  "a boolean (class `bool`)"
})

setOldClass(c("str"))
#' @rdname friendly_class
setMethod("friendly_class", signature("str"), function(object) {
  if (!setequal(class(object), "str")) return(callNextMethod())
  "a string (class `str`)"
})

setOldClass(c("tuple"))
#' @rdname friendly_class
setMethod("friendly_class", signature("tuple"), function(object) {
  if (!setequal(class(object), "tuple")) return(callNextMethod())
  "a tuple (class `tuple`)"
})

setOldClass(c("dict"))
#' @rdname friendly_class
setMethod("friendly_class", signature("dict"), function(object) {
  if (!setequal(class(object), "dict")) return(callNextMethod())
  "a dictionary (class `dict`)"
})

setOldClass(c("set"))
#' @rdname friendly_class
setMethod("friendly_class", signature("set"), function(object) {
  if (!setequal(class(object), "set")) return(callNextMethod())
  "a set (class `set`)"
})
