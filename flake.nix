{
  description = "lf-exa-icons";

  inputs = {
    nixpkgs.url = "nixpkgs/nixpkgs-unstable";
    utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.flake-utils.follows = "utils";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { self, nixpkgs, utils, poetry2nix }:
    utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = import nixpkgs {
            inherit system;
            overlays = [ poetry2nix.overlay ];
          };
        in
        with pkgs; {
          packages = rec {
            default = (pkgs.poetry2nix.mkPoetryApplication {
              projectDir = ./.;
            }).overrideAttrs (oldAttrs: {
              postFixup = oldAttrs.postFixup + ''
                substituteInPlace $out/lib/python3.10/site-packages/lf_exa_icons/main.py \
                  --replace 'build/tree-sitter-rust.so' '${tree-sitter-grammars.tree-sitter-rust}/parser'
              '';
            });

            lf-exa-icons-output = runCommand "lf-exa-icons-output" { } ''
              ${default}/bin/lf-exa-icons ${exa.src}/src/output/icons.rs > $out
            '';
          };

          devShells.default = (pkgs.poetry2nix.mkPoetryEnv {
            projectDir = ./.;
          }).overrideAttrs (oldAttrs: {
            nativeBuildInputs = oldAttrs.nativeBuildInputs ++ [
              poetry
              (python3Packages.python-lsp-server.overrideAttrs (_: {
                # TODO: remove this once it works again
                doInstallCheck = false;
              }))
            ];
          });
        }) // {
      overlays.default = (final: _: {
        lf-exa-icons = self.packages.${final.system}.default;
        lf-exa-icons-output = self.packages.${final.system}.lf-exa-icons-output;
      });
    };
}
