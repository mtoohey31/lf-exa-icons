{
  description = "lf-exa-icons";

  inputs = {
    nixpkgs.url = "nixpkgs/nixpkgs-unstable";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils }: {
    overlays.default = final: _: rec {
      lf-exa-icons = final.python3.pkgs.buildPythonApplication {
        pname = "lf-exa-icons";
        version = "0.1.0";
        src = ./.;
        patchPhase = ''
          substituteInPlace lf_exa_icons/main.py \
            --replace 'build/tree-sitter-rust.so' '${final.tree-sitter-grammars.tree-sitter-rust}/parser'
        '';
        # tests require network access
        doCheck = false;
        propagatedBuildInputs = with final.python3.pkgs; [
          py-tree-sitter
          requests
        ];
      };

      lf-exa-icons-output =
        let
          exa-src = final.applyPatches {
            inherit (final.exa) src patches;
          };
        in
        final.runCommand "lf-exa-icons-output" { } ''
          ${lf-exa-icons}/bin/lf-exa-icons ${exa-src}/src/output/icons.rs > $out
        '';
    };
  } // utils.lib.eachDefaultSystem (system: with import nixpkgs
    { inherit system; overlays = [ self.overlays.default ]; } ; {
    packages = {
      default = lf-exa-icons;
      inherit lf-exa-icons lf-exa-icons-output;
    };

    devShells.default = mkShell {
      packages = [
        (python3.withPackages (ps: with ps; [
          pytest
          python-lsp-server
          py-tree-sitter
          requests
        ]))
      ];
    };
  });
}
