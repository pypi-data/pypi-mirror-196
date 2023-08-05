# Flexible, scalable memory macro generators

In a circuit design often on-chip memories are needed. These blocks are typically custom generated next to the standard cell libraries as building blocks out of standard cells will take too much area.

Purpose of c4m-flexmem module is to have generators that are easily scalable between different technologies using the [PDKMaster](https://gitlab.com/Chips4Makers/PDKMaster) framework. Currently only SRAM generators are included but in the future it is planned to have other types like embedded DRAM, non-volatile, ROM etc.

## Release history

* v0.1.0: Update for [release v0.9.0 of PDKMaster](https://gitlab.com/Chips4Makers/PDKMaster/-/blob/v0.9.0/ReleaseNotes/v0.9.0.md)
* no notes for older releases

## Status

This repository is currently considered experimental code with no backwards compatibility guarantees whatsoever. The library now progresses at the need of tape-outs. 
If interested head over to [gitter](https://gitter.im/Chips4Makers/community) for further discussion.
