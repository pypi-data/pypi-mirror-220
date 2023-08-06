Increment version number in setup.cfg

Build with 
`python -m build` 

(might need to do )
`pip install build`

Then publish with 
`python -m twine upload dist/*`

Might need to do 
`pip install twine`

Generate docs with:
`pdoc3 client.py -o [output path]`
The proper frontend directory should look something like:
`pdoc3 client.py -o /Users/rayan/Documents/playground/playground_fe/public/docs/playgroundrl`
Add `--html` to generate an html version.
