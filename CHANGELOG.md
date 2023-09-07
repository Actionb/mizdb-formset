# Changelog

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