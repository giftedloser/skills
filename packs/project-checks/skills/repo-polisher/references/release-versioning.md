# Release and Versioning Guidance

Ask before changing versions or release notes.

## Versioning

Use Semantic Versioning when the project has a public API or distributed package:

- MAJOR: incompatible API or behavior changes
- MINOR: backward-compatible features
- PATCH: backward-compatible fixes or documentation-only release corrections

For internal tools without public API, preserve the existing versioning convention unless the user requests normalization.

## Changelog

Use Keep a Changelog headings where applicable:

- Added
- Changed
- Deprecated
- Removed
- Fixed
- Security

Do not invent release history. Build changelog entries from commits, existing release notes, or user-provided context.
