#' @importFrom tblcheck hinted_class_message
NULL

setOldClass("py_tbl_df")
setOldClass("py_grouped_df")
#' @rdname hinted_class_message
setMethod("hinted_class_message", signature("py_tbl_df", "py_grouped_df"),
  function(object, expected) {
    paste(
      "I was only expecting 1 value for each grouping in the table," ,
      "but you have multiple values per grouping.",
      "Maybe you are missing a `.groupby()` call?"
    )
  }
)

#' @rdname hinted_class_message
setMethod("hinted_class_message", signature("py_grouped_df", "py_tbl_df"),
  function(object, expected) {
    paste(
      "Your table row labels (i.e. index) are not a numbered sequence.",
      "You can tell by the extra spacing around the column names.",
      "You can fix this with `.reset_index()`"
    )
  }
)