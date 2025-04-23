{
  description = "A Nix flake for pshell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
        };

        pythonEnv = pkgs.python3.withPackages (ps: with ps; [
          setuptools
          wheel
          colorama
          prompt_toolkit
        ]);

        pshell = pkgs.python3Packages.buildPythonPackage rec {
          pname = "pshell";
          version = "0.1.0";
          src = ./.;
          format = "pyproject";

          propagatedBuildInputs = with pkgs.python3Packages; [
            colorama
            prompt_toolkit
          ];

          # If using setup.py instead of pyproject.toml
          build-system = with pkgs.python3Packages; [
            setuptools
          ];

          # Entry point configuration
          pythonImportsCheck = ["psh"];
        };
      in {
        packages.default = pshell;

        apps.default = {
          type = "app";
          program = "${pshell}/bin/psh";
        };

        devShells.default = pkgs.mkShell {
          packages = [ pythonEnv ];
        };
      });
}
