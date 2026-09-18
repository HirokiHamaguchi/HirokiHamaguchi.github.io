import unittest

from .qiita import _convert_qiita_math_fences


class ConvertQiitaMathFencesTest(unittest.TestCase):
    def test_converts_math_fence(self):
        source = "before\n\n```math\nx^2 + y^2 = 1\n```\n\nafter\n"
        expected = "before\n\n$$\nx^2 + y^2 = 1\n$$\n\nafter\n"
        self.assertEqual(_convert_qiita_math_fences(source), expected)

    def test_converts_math_fence_in_blockquote(self):
        source = "> ```math\n> x = 1\n> ```\n"
        expected = "> $$\n> x = 1\n> $$\n"
        self.assertEqual(_convert_qiita_math_fences(source), expected)

    def test_does_not_convert_other_code_fences(self):
        source = "```python\nprint('$x$')\n```\n"
        self.assertEqual(_convert_qiita_math_fences(source), source)

    def test_keeps_unclosed_math_fence(self):
        source = "before\n```math\nx = 1\n"
        self.assertEqual(_convert_qiita_math_fences(source), source)


if __name__ == "__main__":
    unittest.main()
