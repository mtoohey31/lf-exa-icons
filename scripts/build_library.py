from tree_sitter import Language

Language.build_library(
    'build/tree-sitter-rust.so',
    ['vendor/tree-sitter-rust']
)
