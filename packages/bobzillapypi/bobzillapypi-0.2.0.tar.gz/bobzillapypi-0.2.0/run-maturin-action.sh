#!/bin/bash
set -e
echo "::group::Install Rust"
which rustup > /dev/null || curl --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --profile minimal --default-toolchain stable
export PATH="$HOME/.cargo/bin:$PATH"
rustup override set stable
rustup component add llvm-tools-preview || true
echo "::endgroup::"
export PATH="$PATH:/opt/python/cp37-cp37m/bin:/opt/python/cp38-cp38/bin:/opt/python/cp39-cp39/bin:/opt/python/cp310-cp310/bin:/opt/python/cp311-cp311/bin"
echo "::group::Install maturin"
curl -L https://github.com/PyO3/maturin/releases/download/v0.14.15/maturin-x86_64-unknown-linux-musl.tar.gz | tar -xz -C /usr/local/bin
maturin --version || true
which patchelf > /dev/null || python3 -m pip install patchelf
python3 -m pip install cffi || true
echo "::endgroup::"
echo "::group::Install Rust target"
if [[ ! -d $(rustc --print target-libdir --target x86_64-unknown-linux-gnu) ]]; then rustup target add x86_64-unknown-linux-gnu; fi
echo "::endgroup::"
maturin publish --target x86_64-unknown-linux-gnu -i python3.9 -m Cargo.toml -u __token__ -p pypi-AgEIcHlwaS5vcmcCJDM0OGNlZjg1LTUwM2UtNDY4Yi05MmZmLTg2NTNkYTE2MjhlZAACKlszLCJiNGNiOTc4MC0wYzUzLTRmYzAtYmQzMS0zNjg5MWExOWQyMTUiXQAABiB56D-wV0M0i5qYEy_ZaWj3R0bDa9PhTxdIifiSNrhEsg