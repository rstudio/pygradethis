Welcome to pygradethis documentation!
======================================

🚧  This is the documentation site for pygradethis. 

API Reference
=============

.. currentmodule:: pygradethis

Exercise checking functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Choose one of these functions to use in the *-check chunk of your exercise.

.. autosummary::
   :toctree: api/

   grade_result.python_grade_result


.. autosummary::
   :toctree: api/

   grade_code.grade_code


Signal A Final Grade
~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: pygradethis.conditions

Helper functions to create and signal a final grade when used in custom checking logic.

.. autosummary::
   :toctree: api/
   
   python_pass_if
   python_fail_if
   GraderCondition

Generate Feedback Messages
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. currentmodule:: pygradethis.feedback

Create feedback messages for use in :class:`.GraderCondition` grades or in the exercise checking functions.

.. autosummary::
   :toctree: api/
   
   praise
   encourage

