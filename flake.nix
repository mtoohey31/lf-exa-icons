{
  description = "lf-exa-icons";

  inputs = {
    nixpkgs.url = "nixpkgs/nixpkgs-unstable";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils }: {
    overlays.default = final: _: rec {
      lf-exa-icons = (final.poetry2nix.mkPoetryApplication {
        projectDir = ./.;
        overrides = final.poetry2nix.overrides.withDefaults (final: prev: {
          tree-sitter = prev.tree-sitter.overridePythonAttrs (oldAttrs: {
            propagatedBuildInputs = oldAttrs.propagatedBuildInputs ++ [
              prev.setuptools
            ];
          });
        });
      }).overrideAttrs (oldAttrs: {
        postFixup = oldAttrs.postFixup + ''
          substituteInPlace $out/lib/python3.10/site-packages/lf_exa_icons/main.py \
            --replace 'build/tree-sitter-rust.so' '${final.tree-sitter-grammars.tree-sitter-rust}/parser'
        '';
      });

      lf-exa-icons-output = final.runCommand "lf-exa-icons-output" { } ''
        ${lf-exa-icons}/bin/lf-exa-icons ${final.exa.src}/src/output/icons.rs > $out
      '';
    };
  } // utils.lib.eachDefaultSystem (system: with import nixpkgs
    { inherit system; overlays = [ self.overlays.default ]; } ; {
    packages = {
      default = lf-exa-icons;
      inherit lf-exa-icons lf-exa-icons-output;
    };

    devShells.default = lf-exa-icons.dependencyEnv.overrideAttrs (oldAttrs: {
      nativeBuildInputs = oldAttrs.nativeBuildInputs ++ [
        gcc
        poetry
        python3
        python3Packages.python-lsp-server
      ];
    });
  });
}
