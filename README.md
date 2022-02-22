Japanese follows English （日本語は英語の後にあります）

# boto3-stubs-reducer

This boto3-stubs-reducer helps PyCharm to make implicit type estimation of boto3-stubs. 
Actually, boto3-stubs-reducer reduces @overload in boto3-stubs.

Currently, [PyCharm can't handle many @overload](https://youtrack.jetbrains.com/issue/PY-40997) and implicit type estimation does not work.

But actually, not all boto3-stubs are installed. boto3-stubs installs only "essential" services (ec2, s3, etc.) by default.

This boto3-stubs-reducer reduces @overload in boto3-stubs in your Python library path. boto3-stubs-reducer remains only @overload with mypy type definition is installed. After running boto3-stubs-reducer, PyCharm can guess boto3 client and resource types without explicit type hinting.

## Usage

Install using `pip install boto3-stubs-reducer`, and run `boto3-stubs-reducer`.

```bash
$ pip install boto3 boto3-stubs[essential]
$ pip install boto3-stubs-reducer
$ boto3-stubs-reducer
reduce /Users/smatsumoto/tmp/boto3-stubs-reducer/venv/lib/python3.9/site-packages/boto3-stubs/__init__.pyi
reduce /Users/smatsumoto/tmp/boto3-stubs-reducer/venv/lib/python3.9/site-packages/boto3-stubs/session.pyi
Replacing boto3-stubs successfully.
```

Then your PyCharm can guess boto3.session.client() and resource() return value without explit type hinting.

If you want to revert changes, you can run it with `-r` option.

```bash
$ boto3-stubs-reducer -r
revert /Users/smatsumoto/tmp/boto3-stubs-reducer/venv/lib/python3.9/site-packages/boto3-stubs/__init__.pyi
revert /Users/smatsumoto/tmp/boto3-stubs-reducer/venv/lib/python3.9/site-packages/boto3-stubs/session.pyi
Original boto3-stubs is reverted successfully.
```

## Notes

- If the script helps you, I'm glad staring on PyPI and GitHub repository!
- If you encountered troubles, and/or you have any suggestion or comment, please let me know via Twitter @smatsumt

# (日本語)

このスクリプトは、PyCharm で boto3-stubs の暗黙の型推論ができない問題に対処するためのものです。具体的には、boto3-stubs の boto3.Session.client(), boto3.Session.resource() の大量の @overload 指定を、実際に mypy が入っている、今使っているものだけを残すようにします。

boto3-stubs の @overload 指定は、boto3 がサポートしているすべての AWS サービスの分が定義されています。が、そのために @overload 指定が大量にあって PyCharm の暗黙の型推論が動作しません。 2022/02 現在、この問題は解決しておらず [PyCharm は大量の @overload をうまく処理できません](https://youtrack.jetbrains.com/issue/PY-40997) 。

boto3-stubs-reducer では、mypy で型定義が入っているモジュールのみに @overload を絞ることで、PyCharm の暗黙の型推論が動くようにします。

## 使い方

`pip` で `boto3-stubs-reducer` をインストール後、`boto3-stubs-reducer` を実行してください。

```bash
$ pip install boto3-stubs-reducer
$ boto3-stubs-reducer
reduce /Users/smatsumoto/tmp/boto3-stubs-reducer/venv/lib/python3.9/site-packages/boto3-stubs/__init__.py
reduce /Users/smatsumoto/tmp/boto3-stubs-reducer/venv/lib/python3.9/site-packages/boto3-stubs/__init__.pyi
reduce /Users/smatsumoto/tmp/boto3-stubs-reducer/venv/lib/python3.9/site-packages/boto3-stubs/session.pyi
Replacing boto3-stubs successfully.
```

これで、PyCharm の暗黙の型推論が動作するようになります。

デフォルトでは、boto3 が入っているライブラリパスを探して、そのライブラリパスの boto3-stubs を対象にします。対象とするライブラリパスを変更する場合は `-p venv/lib/python3.9/site-packages` と、`-p` オプションでパスを指定してください。

元のファイルの復元は、`-r` オプションでできます。

```bash
$ boto3-stubs-reducer -r
revert /Users/smatsumoto/tmp/boto3-stubs-reducer/venv/lib/python3.9/site-packages/boto3-stubs/__init__.py
revert /Users/smatsumoto/tmp/boto3-stubs-reducer/venv/lib/python3.9/site-packages/boto3-stubs/__init__.pyi
revert /Users/smatsumoto/tmp/boto3-stubs-reducer/venv/lib/python3.9/site-packages/boto3-stubs/session.pyi
Original boto3-stubs is reverted successfully.
```

## その他

- もしこのライブラリが役に立ちましたら、PyPi, GitHub でのスターをつけてもらえると嬉しいです！
- うまく動かなかったり、ご提案やコメントなどありましたら Twitter @smatsumt までお願いします。
