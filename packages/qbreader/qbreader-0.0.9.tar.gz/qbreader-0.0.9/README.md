# QBreader Python API wrapper module
Accessing the QBreader API with a python wrapper module.

## Documentation

#### Get a list of sets from the QBreader database 

```
  set_list()
```

This function gets a list of sets from the QBreader database.

#### Search the QBreader database

```
  query()
```
This function searches the QBreader database for questions that match the parameters specified.

| Parameter | Type     |Values| Description                |
| :-------- | :------- |:----------|:------------------------- |
| `questionType` | `string` |`tossup`, `bonus`, `all`| The type of question to search for. Defaults to "all". If one of the three is not set, returns a 400 Bad Request. |
| `searchType` | `string` |`question`, `answer`| The type of search to perform. Defaults to "all". If one of the three is not set, returns a 400 Bad Request. |
| `queryString` | `string` |Any string.| The string to search for. Defaults to "". |
| `regex` | `bool` |`True`, `False`| Whether or not to use regular expressions for the queryString. Defaults to "False". |
| `randomize` | `bool` |`True`, `False`| Whether or not to randomize the order of the results. Defaults to "False". |
| `setName` | `string` |Any string| The difficulties to search for. Defaults to []. Leave as an empty list to search all. Must be a list of ints from 1 to 10. |
| `difficulties` | `list`|`[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`| The string to search for. Defaults to "". |
| `categories` | `list` |See https://pastebin.com/McVDGDXg for a full list.| The categories to search for. Defaults to []. Leave as an empty list to search all. |
| `subcategories` | `list` |See https://pastebin.com/McVDGDXg for a full list.| The subcategories to search for. Defaults to []. Leave as an empty list to search all. |
| `maxQueryReturnLength` | `int` |Any integer. | The maximum number of questions to return. Defaults to None. Leave blank to return 50. Anything over 200 will not work. |


#### Get a random question from the QBreader database

```
  random_question()
```
This function gets a random question from the QBreader database.

| Parameter | Type     |Values| Description                |
| :-------- | :------- |:----------| :------------------------- |
| `questionType` | `string` |`tossup`, `bonus`| The type of question to search for (tossup or bonus). If one of the two is not set, returns a 400 Bad Request. |
| `difficulties` | `list` |`[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]`| The string to search for. Defaults to "". |
| `categories` | `list` |See https://pastebin.com/McVDGDXg for a full list.| The categories to search for. Defaults to []. Leave as an empty list to search all. |
| `subcategories` | `list` |See https://pastebin.com/McVDGDXg for a full list.| The subcategories to search for. Defaults to []. Leave as an empty list to search all. |
| `number` | `int` |Any integer. | The number of questions to return. Defaults to None. Leave blank to return 1.|

#### Generate a random name 

```
  random_question()
```
This function Generates an adjective-noun pair (used in multiplayer lobbies)

#### Get questions from a packet from the QBreader database

```
  packet()
```
This function gets questions from a packet from the QBreader database.

| Parameter | Type     | Values |Description                |
| :-------- | :------- | :---------|:------------------------- |
| `setName` | `string` |Names of sets can be obtained by running set_list()| The name of the set to search. Can be obtained from set_list().|
| `packetNumber` | `int` |Any integer that corresponds to a packet number, usually from 1-11.|The number of the packet to search for.|

#### Get a packet's tossups from the QBreader database

```
  packet_tossups()
```
This function gets a packet's tossups from the QBreader database. Twice as fast as using packet().

| Parameter | Type     | Values |Description                |
| :-------- | :------- | :---------|:------------------------- |
| `setName` | `string` |Names of sets can be obtained by running set_list()| The name of the set to search. Can be obtained from set_list().|
| `packetNumber` | `int` |Any integer that corresponds to a packet number, usually from 1-11.|The number of the packet to search for.|

#### Get a packet's bonuses from the QBreader database

```
  packet_bonuses()
```
This function gets a packet's bonuses from the QBreader database. Twice as fast as using packet().

| Parameter | Type     | Values |Description                |
| :-------- | :------- | :---------|:------------------------- |
| `setName` | `string` |Names of sets can be obtained by running set_list()| The name of the set to search. Can be obtained from set_list().|
| `packetNumber` | `int` |Any integer that corresponds to a packet number, usually from 1-11.|The number of the packet to search for.|

#### Get the number of packets in a set from the QBreader database

```
  packet_bonuses()
```
This function gets the number of packets in a set from the QBreader database

| Parameter | Type     | Values |Description                |
| :-------- | :------- | :---------|:------------------------- |
| `setName` | `string` |Names of sets can be obtained by running set_list()| The name of the set to search. Can be obtained from set_list().|


#### Report a question from the QBreader database

```
  report_question()
```
This function reports a question from the QBreader database.

| Parameter | Type     |Values| Description                |
| :-------- | :------- |:------| :------------------------- |
| `_id` | `string` |Can be obtained from the `query()`, `random_question`, `packet()`, `packet_bonuses`, or `packet_tossups`.| The ID of the question to report.|
| `reason` | `string` |N/A| The reason for reporting the question. Defaults to None. |
| `description` | `string` |N/A| A description of the reason for reporting the question. Defaults to None.|

#### Get a list of rooms from the QBreader database

```
  room_list()
```
This function gets a list of rooms from the QBreader database.