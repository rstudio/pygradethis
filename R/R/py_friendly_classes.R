#' @importFrom tblcheck friendly_class
NULL

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

#' @rdname friendly_class
setMethod("friendly_class", signature("int"), function(object) {
  if (!setequal(class(object), "int")) return(callNextMethod())
  "an integer (class `int`)"
})

#' @rdname friendly_class
setMethod("friendly_class", signature("float"), function(object) {
  if (!setequal(class(object), "float")) return(callNextMethod())
  "a floating point number (class `float`)"
})

#' @rdname friendly_class
setMethod("friendly_class", signature("bool"), function(object) {
  if (!setequal(class(object), "bool")) return(callNextMethod())
  "a boolean (class `bool`)"
})

#' @rdname friendly_class
setMethod("friendly_class", signature("str"), function(object) {
  if (!setequal(class(object), "str")) return(callNextMethod())
  "a string (class `str`)"
})

#' @rdname friendly_class
setMethod("friendly_class", signature("tuple"), function(object) {
  if (!setequal(class(object), "tuple")) return(callNextMethod())
  "a tuple (class `tuple`)"
})

#' @rdname friendly_class
setMethod("friendly_class", signature("dict"), function(object) {
  if (!setequal(class(object), "dict")) return(callNextMethod())
  "a dictionary (class `dict`)"
})