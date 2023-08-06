# mkdocs-blogging-plugin

A mkdocs plugin that generates a blog page listing selected pages, sorted by time. It supports:

- Automatic blog page generation
- Tags
- Category-level customization
- Template-based customization

Demo site: https://liang2kl.github.io/mkdocs-blogging-plugin-example

![preview](https://s2.loli.net/2021/12/03/GqhwCYTsimlkXK1.png)

## Prerequisites

- Only `material` theme is adapted by far
- `navigation.instant` feature cannot be enabled if blog paging is on

Pull requests are welcome to break these constraints.

## Installation

```shell
# macOS or Linux
pip3 install mkdocs-blogging-plugin

# Windows
pip install mkdocs-blogging-plugin
```

## Usage

A complete guide is available at https://liang2kl.github.io/mkdocs-blogging-plugin.

The easiest way to setup everything from scratch is generating your project from [the template repository](https://github.com/liang2kl/mkdocs-blogging-plugin-bootstrap).

## Credits

Inspired by [mkdocs-git-revision-date-localized-plugin](https://github.com/timvink/mkdocs-git-revision-date-localized-plugin) and [mkdocs-material-blog](https://github.com/vuquangtrong/mkdocs-material-blog).
