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
  "an `int`"
})