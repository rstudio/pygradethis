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

setOldClass(c("py_int", "pygradethis"))
#' @rdname friendly_class
setMethod("friendly_class", signature("py_int"), function(object) {
  if (!setequal(class(object), c("py_int", "pygradethis"))) return(callNextMethod())
  "an integer (class `int`)"
})

setOldClass(c("py_float", "pygradethis"))
#' @rdname friendly_class
setMethod("friendly_class", signature("py_float"), function(object) {
  if (!setequal(class(object), c("py_float", "pygradethis"))) return(callNextMethod())
  "a floating point number (class `float`)"
})

setOldClass(c("py_complex", "pygradethis"))
#' @rdname friendly_class
setMethod("friendly_class", signature("py_complex"), function(object) {
  if (!setequal(class(object), c("py_complex", "pygradethis"))) return(callNextMethod())
  "a complex number (class `complex`)"
})

setOldClass(c("py_bool", "pygradethis"))
#' @rdname friendly_class
setMethod("friendly_class", signature("py_bool"), function(object) {
  if (!setequal(class(object), c("py_bool", "pygradethis"))) return(callNextMethod())
  "a boolean (class `bool`)"
})

setOldClass(c("py_str", "pygradethis"))
#' @rdname friendly_class
setMethod("friendly_class", signature("py_str"), function(object) {
  if (!setequal(class(object), c("py_str", "pygradethis"))) return(callNextMethod())
  "a string (class `str`)"
})

setOldClass(c("py_tuple", "pygradethis"))
#' @rdname friendly_class
setMethod("friendly_class", signature("py_tuple"), function(object) {
  if (!setequal(class(object), c("py_tuple", "pygradethis"))) return(callNextMethod())
  "a tuple (class `tuple`)"
})

setOldClass(c("py_dict", "pygradethis"))
#' @rdname friendly_class
setMethod("friendly_class", signature("py_dict"), function(object) {
  if (!setequal(class(object), c("py_dict", "pygradethis"))) return(callNextMethod())
  "a dictionary (class `dict`)"
})

setOldClass(c("py_set", "pygradethis"))
#' @rdname friendly_class
setMethod("friendly_class", signature("py_set"), function(object) {
  if (!setequal(class(object), c("py_set", "pygradethis"))) return(callNextMethod())
  "a set (class `set`)"
})
