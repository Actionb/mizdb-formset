# Changelog

## [unreleased]

- fix form being saved even with invalid formsets

## 0.2.5 (2023-10-10)

- delete button now disables/enables select form elements
- rework InlineFormsetMixin:
    - check formset validity in `post` method instead of `form_valid`
    - save formsets in `post` method instead of in `formset_valid`
    - replace `formset_valid` hook with `post_save` hook

## 0.2.4 (2023-10-04)

- scroll new forms into view when clicking the add button
- InlineFormsetMixin: do not use form kwargs as formset kwargs.
  The `initial` argument for formsets must be a list of dicts, whereas for forms it must be a dict. Re-using the kwargs
  from `get_form_kwargs` on a formset
  resulted in an error, because `initial` (if specified by the view) would be a dict.

## 0.2.3 (2023-09-07)

### Changed

- the combined media now includes the media of the view's model form - this is to avoid
  including resources that are shared by both formset and form multiple times
- the combined media is now available under the name `combined_media`

## 0.2.2 (2023-09-06)

### Changed

- Changed CSS class for the 'add' button to `inline-add-btn` to make it more specific
- Changed CSS class for the 'delete' button to `inline-delete-btn`

## 0.2.1 (2023-09-04)

### Fixed

- exception from collecting media with an empty formset list

## 0.2.0 (2023-09-01)

### added

- the combined media of all formsets is now available to the template context under the name `formset_media`
- the add button text can now be modified using the `add_text` keyword argument for `InlineFormsetRenderer`

## 0.1.0 (2023-08-31)

- initial release