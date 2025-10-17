# HirokiHamaguchi.github.io

This is my personal website.

[https://hirokihamaguchi.github.io/](https://hirokihamaguchi.github.io/)

This repository uses the template of [Academic Pages](https://github.com/academicpages/academicpages.github.io)

## ToDo

note folder is not reflected in the website. I will fix it.

## How to Run Locally

```bash
gem install bundler
bundle config set --local path 'vendor/bundle'
bundle install
uv run gen/gen.py
bundle exec jekyll serve -l -H localhost
```

## LICENSE

We use the MIT License. Please see the [LICENSE](LICENSE) file for details.
