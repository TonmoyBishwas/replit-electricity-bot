{ pkgs }: {
  deps = [
    pkgs.python3
    pkgs.python3Packages.pip
    pkgs.chromium
    pkgs.chromedriver
  ];
}