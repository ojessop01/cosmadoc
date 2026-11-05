# StorJ cloud storage (hosted on DiRAC nodes)

A quota allocation on the [StorJ cloud system](https://satellite.storj.cosma.dur.ac.uk/) is available for users who wish to share their data with selected colleagues who do not have a COSMA account.  Please ask if you would like to use this.  This can expose Object buckets via a standard S3 backend, or via a faster StorJ interface.

## StorJ usage

After logging in to the web interface, you will be presented with a project dashboard.  Within this, you can create projects (please ask if you would like your limit increasing), and within the projects, can create buckets for upload of data.  You can upload data via the web interface, or using the rclone tool.

### rclone

On a COSMA login node, first `module load rclone`.

To set a new end point (you need to do this for each bucket and project you with to interact with), use `rclone config`.  Then follow these steps:

```
n) to create a new remote
name> Give it a name (e.g. mybucket)
Select the S3 or StorJ backend (option 5 or 41 respectively at the time of writing, respectively)
```

You will then be presented with options specific for the back end.

#### For a S3 backend:

```
For the provider, select StorJ (option 20)
Enter your credentials (you can get this from the web interface: Access keys option in the left hand menu):
1> Enter AWS credentials
access_key_id> Copy the access key
secret_access_key> Copy the secret
endpoint> https://gateway-mt.storj.cosma.dur.ac.uk
Edit advanced config? Select n.
Yes this is OK> y
```

#### For the StorJ backend:

```
2> Create a new access grant  (select the API Key option within the web interface)
```

For the `satellite address>` option, copy this from the web interface, but replace `api.storj.cosma.dur.ac.uk:7777` with `172.17.185.195:7777`.

Enter the API key when prompted.

We recommend you choose a passphrase.

And "y" to save the config.

Once you have chosen a phassphrase, you will also need to use this in the [web interface](https://satellite.storj.cosma.dur.ac.uk/login) (if you use this).  Here, select "Project" (top of the side bar) -> "Manage passphrase" -> "Switch active passphrase".

#### Using rclone

You can then use commands such as:

- `rclone lsf mybucket:` to list a bucket
- `rclone mkdir mybucket:mydir` to make a directory
- `rclone copy myfile mybucket:mydir/` to copy a file to it
- etc


## The uplink command

The uplink command ([available to download from StorJ](https://storj.dev/dcs/api/uplink-cli/installation), or in the storj module on COSMA)  can be used instead of S3 tools.

`uplink access setup --use`

1. Give a name for your setup.
2. Enter the Access grant that you obain from the web interface.
3. N to not use S3 backwards-compatible gateway credentials.

`uplink access list`

Shows the current keys.

`uplink ls`

Shows files within this storage.

`uplinke mb sj://demo`

Make bucket (mb) of type sj, name demo.

`uplink ls`

Will now show the bucket (a bit loke a directory).

`echo "My file contents" | uplink cp --progress=false - sj://demo/file.txt`

To create a file.

`uplink ls sj://demo`

Then shows the contents of the demo bucket.

## Using the metadata client

`metaclient`

Available commands are get, set, rm and search.

```
export STORJ_METASEARCH_SERVER=https://metasearch.storj.cosma.dur.ac.uk
export STORJ_METASEARCH_ACCESS="$(jq -r '.accesses[.default]' ~/.config/storj/uplink/access.json)"
```

Get metadata on a file:

`metaclient get sj://demo/file.txt`

Set some metadata:

`metaclient set sj://demo/file.txt -d '{"project":"cosma", "dataset":"halo-catalogue", "run":1, "tags":["dm","sim"]}'
`

`metaclient get sj://demo/file.txt`

Search for metadata

`metaclient search sj://demo --match '{"dataset":"halo-catalogue"}'`

As an array:

`metaclient search sj://demo --match '{"tags":["obs"]}'`

Filtering

``metaclient search sj://demo --match '{"project":"cosma"}' --filter 'run > `1`' ``

Projections

`metaclient search sj://demo --match  '{"project":"cosma"} --projection '{ds: dataset, r:run}`

Getting metadata with uplink

`uplink meta get sj://demo/file.txt`


Deleting (removing) buckets

`uplink rb --force sj://demo`

Accessing multiple buckets


`uplink access list;`
`uplink access use dirac;`
`uplink access remove demo`


# Scope

1. Temporary offloading data from DiRAC services
2. Transfering, sharing, collaborating, within DiRAC, between DiRAC and internationally

Storage beyond the end of a DiRAC project is not supported.  



# Storage allocation

Apply during annual RAC calls, with an initial call in October 2026.

# Encryption

Data are encrypted, and only you and collaborators have the encryption key.  If you lose your key, we cannot help!




# DiRAC StorJ Terms of service

To be added.

# DiRAC StorJ Privacy Policy

To be added.



