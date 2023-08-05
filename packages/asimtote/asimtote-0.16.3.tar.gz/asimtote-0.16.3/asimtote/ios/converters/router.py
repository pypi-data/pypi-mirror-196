# asimtote.ios.converters.router
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



# --- imports ---



import netaddr

from deepops import deepget

from ...diff import DiffConvert



# --- converter classes ---



# ip[v6] route ...



class Cvt_IPRoute(DiffConvert):
    cmd = "ip-route", None, None, None

    def _cmd(self, vrf, net, r):
        n = netaddr.IPNetwork(net)

        return ("ip route"
                + ((" vrf " + vrf) if vrf else "")
                + " " + str(n.network) + " " + str(n.netmask)
                + ((" " + r["interface"]) if "interface" in r else "")
                + ((" " + r["router"]) if "router" in r else "")
                + ((" %d" % r["metric"]) if "metric" in r else "")
                + ((" tag %d" % r["tag"]) if "tag" in r else ""))

    def remove(self, old, vrf, net, id):
        return "no " + self._cmd(vrf, net, old)

    def update(self, old, upd, new, vrf, net, id):
        return self._cmd(vrf, net, new)


class Cvt_IPv6Route(DiffConvert):
    cmd = "ipv6-route", None, None, None

    def _cmd(self, vrf, net, r):
        return ("ipv6 route"
                + ((" vrf " + vrf) if vrf else "")
                + " " + net
                + ((" " + r["interface"]) if "interface" in r else "")
                + ((" " + r["router"]) if "router" in r else "")
                + ((" " + str(r["metric"])) if "metric" in r else "")
                + ((" tag " + str(r["tag"])) if "tag" in r else ""))

    def remove(self, old, vrf, net, id):
        return "no " + self._cmd(vrf, net, old)

    def update(self, old, upd, new, vrf, net, id):
        return self._cmd(vrf, net, new)



# route-map ...



class Cvt_RtMap(DiffConvert):
    cmd = "route-map", None
    block = "rtmap-del"

    def remove(self, old, rtmap):
        return "no route-map " + rtmap


class DiffConvert_RtMap(DiffConvert):
    context = Cvt_RtMap.cmd


class Cvt_RtMap_Entry(DiffConvert_RtMap):
    cmd = None,
    block = "rtmap-del"

    def remove(self, old, rtmap, seq):
        return "no route-map %s %d" % (rtmap, seq)


class Cvt_RtMap_Entry_Action(DiffConvert_RtMap):
    cmd = None, "action"
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        return "route-map %s %s %d" % (rtmap, new, seq)


class DiffConvert_RtMap_Entry(DiffConvert_RtMap):
    context = DiffConvert_RtMap.context + Cvt_RtMap_Entry.cmd

    def enter(self, rtmap, rtmap_dict, seq):
        return ["route-map %s %s %d" % (rtmap, rtmap_dict["action"], seq)]


class Cvt_RtMap_MatchCmty_DelExact(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "community", "exact-match"
    block = "rtmap-del"
    trigger_blocks = { "rtmap-add-cmty" }

    # if removing the exact-match option, we need to clear the list and
    # recreate it without it
    def remove(self, old, rtmap, seq):
        if self.get_ext(old):
            l = self.enter(rtmap, old, seq)
            l.append(" no match community")
            return l


class DiffConvert_RtMap_MatchCmty(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "community", "communities", None


class Cvt_RtMap_MatchCmty_Del(DiffConvert_RtMap_MatchCmty):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq, cmty):
        l = self.enter(rtmap, old, seq)
        l.append(" no match community " + cmty)
        return l


class Cvt_RtMap_MatchCmty_add(DiffConvert_RtMap_MatchCmty):
    block = "rtmap-add-cmty"

    def update(self, old, upd, new, rtmap, seq, cmty):
        # TODO: need to handle applying 'exact-match' when list is the
        # same; will rework these to use split_args_offset to see if
        # that makes it easier (as we need the action from a higher
        # context but would like to set a lower context)
        l = self.enter(rtmap, new, seq)
        exact_match = deepget(new, "match", "community", "exact-match")
        l.append(" match community %s%s"
                     % (cmty, " exact-match" if exact_match else ""))
        return l

    def trigger(self, new, *args):
        return self.update(new, new, new, *args)


class Cvt_RtMap_MatchIPAddr(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "ip-address"

class Cvt_RtMap_MatchIPAddr_Del(Cvt_RtMap_MatchIPAddr):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        for addr in sorted(self.get_ext(rem)):
            l.append(" no match ip address " + addr)
        return l

class Cvt_RtMap_MatchIPAddr_Add(Cvt_RtMap_MatchIPAddr):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        for addr in sorted(self.get_ext(upd)):
            l.append(" match ip address " + addr)
        return l


class Cvt_RtMap_MatchIPPfxLst(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "ip-prefix-list"

class Cvt_RtMap_MatchIPPfxLst_Del(Cvt_RtMap_MatchIPPfxLst):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        for pfx in sorted(self.get_ext(rem)):
            l.append(" no match ip address prefix-list " + pfx)
        return l

class Cvt_RtMap_MatchIPPfxLst_Add(Cvt_RtMap_MatchIPPfxLst):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        for pfx in sorted(self.get_ext(upd)):
            l.append(" match ip address prefix-list " + pfx)
        return l


class Cvt_RtMap_MatchIPv6Addr(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "ipv6-address"

class Cvt_RtMap_MatchIPv6Addr_Del(Cvt_RtMap_MatchIPv6Addr):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        for addr in sorted(self.get_ext(rem)):
            l.append(" no match ipv6 address " + addr)
        return l

class Cvt_RtMap_MatchIPv6Addr_Add(Cvt_RtMap_MatchIPv6Addr):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        for addr in sorted(self.get_ext(upd)):
            l.append(" match ipv6 address " + addr)
        return l


class Cvt_RtMap_MatchIPv6PfxLst(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "ipv6-prefix-list"

class Cvt_RtMap_MatchIPv6PfxLst_Del(Cvt_RtMap_MatchIPv6PfxLst):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        for pfx in sorted(self.get_ext(rem)):
            l.append(" no match ipv6 address prefix-list " + pfx)
        return l

class Cvt_RtMap_MatchIPv6PfxLst_Add(Cvt_RtMap_MatchIPv6PfxLst):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        for pfx in sorted(self.get_ext(upd)):
            l.append(" match ipv6 address prefix-list " + pfx)
        return l


class Cvt_RtMap_MatchTag(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "match", "tag"

class Cvt_RtMap_MatchTag_Del(Cvt_RtMap_MatchTag):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        for tag in sorted(self.get_ext(rem)):
            l.append(" no match tag " + str(tag))
        return l

class Cvt_RtMap_MatchTag_Add(Cvt_RtMap_MatchTag):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        for tag in sorted(self.get_ext(upd)):
            l.append(" match tag " + str(tag))
        return l


class Cvt_RtMap_SetCmty(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "set", "community", "communities"

class Cvt_RtMap_SetCmty_Del(Cvt_RtMap_SetCmty):
    block = "rtmap-del"

    def truncate(self, old, rem, new, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        for cmty in sorted(self.get_ext(rem)):
            l.append(" no set community " + cmty)
        return l

class Cvt_RtMap_SetCmty_Add(Cvt_RtMap_SetCmty):
    block = "rtmap-add"

    # TODO: need to handle case where list is the same but 'additive'
    # is only addition or removal
    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        for cmty in sorted(self.get_ext(upd)):
            l.append(" set community "
                     + cmty
                     + (" additive" if "additive" in new["set"]["community"]
                            else ""))
        return l


class Cvt_RtMap_SetIPNxtHop(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "set", "ip-next-hop"

    def _cmd(self, nexthop):
        addr = nexthop["addr"]
        vrf = None
        if "vrf" in nexthop:
            vrf = ("vrf " + nexthop["vrf"]) if nexthop["vrf"] else "global"

        return "set ip" + ((" " + vrf) if vrf else "") + " next-hop " + addr

class Cvt_RtMap_SetIPNxtHop_Del(Cvt_RtMap_SetIPNxtHop):
    block = "rtmap-del"

    def remove(self, old, rtmap, seq):
        # we must remove all the 'set ip next-hop' commands individually
        l = self.enter(rtmap, old, seq)
        for nexthop in self.get_ext(old):
            l.append(" no " + self._cmd(nexthop))
        return l

class Cvt_RtMap_SetIPNxtHop_Add(Cvt_RtMap_SetIPNxtHop):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        # the 'set ip ... next-hop' commands are an ordered list and, if
        # anything has changed, we need to destroy the old one and
        # create the new one from scratch
        l = self.enter(rtmap, new, seq)
        if old:
            for old_nexthop in self.get_ext(old):
                l.append(" no " + self._cmd(old_nexthop))
        for new_nexthop in self.get_ext(new):
            l.append(" " + self._cmd(new_nexthop))
        return l


class Cvt_RtMap_SetIPNxtHopVrfy(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "set", "ip-next-hop-verify-availability"

    def remove(self, old, rtmap, seq):
        l = self.enter(rtmap, old, seq)
        l.append(" no set ip next-hop verify-availability")
        return l

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)
        l.append(" set ip next-hop verify-availability")
        return l

class Cvt_RtMap_SetIPNxtHopVrfyTrk(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "set", "ip-next-hop-verify-availability-track", None

    def _cmd(self, seq, nexthop):
        return ("set ip next-hop verify-availability %s %s track %d"
                     % (nexthop["addr"], seq, nexthop["track-obj"]))

class Cvt_RtMap_SetIPNxtHopVrfy_Del(Cvt_RtMap_SetIPNxtHopVrfyTrk):
    block = "rtmap-del"

    def remove(self, old, rtmap, seq, nexthop_seq):
        return self.enter(rtmap, old, seq) + [
                   " no "
                       + self._cmd(nexthop_seq,
                                   self.get_ext(old, nexthop_seq))]

class Cvt_RtMap_SetIPNxtHopVrfy_Add(Cvt_RtMap_SetIPNxtHopVrfyTrk):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq, nexthop_seq):
        # individual entries (ordered by sequence number) can be replaced but
        # the old entry must be removed first, before the new one added
        l = self.enter(rtmap, new, seq)
        if old:
            l.append(" no "
                     + self._cmd(nexthop_seq, self.get_ext(old, nexthop_seq)))
        l.append(" " + self._cmd(nexthop_seq, self.get_ext(new, nexthop_seq)))
        return l


class Cvt_RtMap_SetIPv6NxtHop(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "set", "ipv6-next-hop"

    def _cmd(self, nexthop):
        addr = nexthop["addr"]
        return "set ipv6 next-hop " + addr

class Cvt_RtMap_SetIPv6NxtHop_Del(Cvt_RtMap_SetIPv6NxtHop):
    block = "rtmap-del"

    def remove(self, old, rtmap, seq):
        # we must remove all the 'set ipv6 next-hop' commands individually
        l = self.enter(rtmap, old, seq)
        for nexthop in self.get_ext(old):
            l.append(" no " + self._cmd(nexthop))
        return l

class Cvt_RtMap_SetIPv6NxtHop_Add(Cvt_RtMap_SetIPv6NxtHop):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        # the 'set ip ... next-hop' commands are an ordered list and, if
        # anything has changed, we need to destroy the old one and
        # create the new one from scratch
        l = self.enter(rtmap, new, seq)
        if old:
            for old_nexthop in self.get_ext(old):
                l.append(" no " + self._cmd(old_nexthop))
        for new_nexthop in self.get_ext(new):
            l.append(" " + self._cmd(new_nexthop))
        return l


class Cvt_RtMap_SetLocalPref(DiffConvert_RtMap_Entry):
    cmd = tuple()
    ext = "set", "local-preference"

class Cvt_RtMap_SetLocalPref_Del(Cvt_RtMap_SetLocalPref):
    block = "rtmap-del"

    def remove(self, old, rtmap, seq):
        return self.enter(rtmap, old, seq) + [" no set local-preference"]

class Cvt_RtMap_SetLocalPref_Add(Cvt_RtMap_SetLocalPref):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        return self.enter(rtmap, new, seq) + [
                   " set local-preference " + str(self.get_ext(new))]


class Cvt_RtMap_SetVRF(DiffConvert_RtMap_Entry):
    # this handles both 'set global' and 'set vrf ...'
    cmd = tuple()
    ext = "set", "vrf"

    def _cmd(self, entry):
        vrf = self.get_ext(entry)
        return "set " + (("vrf " + vrf) if vrf else "global")

class Cvt_RtMap_SetVRF_Del(Cvt_RtMap_SetVRF):
    block = "rtmap-del"

    def remove(self, old, rtmap, seq):
        return self.enter(rtmap, old, seq) + [" no " + self._cmd(old)]

class Cvt_RtMap_SetVRF_Add(Cvt_RtMap_SetVRF):
    block = "rtmap-add"

    def update(self, old, upd, new, rtmap, seq):
        l = self.enter(rtmap, new, seq)

        # if there's a previous setting, and we're changing from global
        # to a VRF, or vice-versa, we need to clear the old setting
        # first
        if old and (bool(self.get_ext(old)) != bool(self.get_ext(new))):
            l.append(" no " + self._cmd(old))

        l.append(" " + self._cmd(new))
        return l



# router ospf ...



class Cvt_RtrOSPF(DiffConvert):
    cmd = "router", "ospf", None

    def remove(self, old, proc):
        return "no router ospf " + str(proc)

    def add(self, new, proc):
        return "router ospf " + str(proc)


class DiffConvert_RtrOSPF(DiffConvert):
    context = "router", "ospf", None

    def enter(self, proc):
        return ["router ospf " + str(proc)]


class Cvt_RtrOSPF_Id(DiffConvert_RtrOSPF):
    cmd = "id",

    def remove(self, old, proc):
        return self.enter(proc) + [" no router-id"]

    def update(self, old, upd, new, proc):
        return self.enter(proc) + [" router-id " + new]


class Cvt_RtrOSPF_AreaNSSA(DiffConvert_RtrOSPF):
    cmd = "area", None, "nssa"

    def remove(self, old, proc, area):
        return self.enter(proc) + [" no area %s nssa" % area]

    def truncate(self, old, upd, new, proc, area):
        # if we're truncating, we're removing options and we do that by
        # just re-entering the command without them, same as update()
        return self.update(old, None, new, proc, area)

    def update(self, old, upd, new, proc, area):
        s = ""
        if "no-redistribution" in new: s += " no-redistribution"
        if "no-summary" in new: s += " no-summary"
        return self.enter(proc) + [" area %s nssa%s" % (area, s)]


# passive-interface configuration is slightly odd as the default mode is
# stored (assuming it's not the default) and then a list of exceptions
# is maintained and it can go either way


class Cvt_RtrOSPF_PasvInt_Dflt(DiffConvert_RtrOSPF):
    cmd = "passive-interface", "default"

    def remove(self, old, proc):
        return self.enter(proc) + [" no passive-interface default"]

    def update(self, old, upd, new, proc):
        return self.enter(proc) + [" passive-interface default"]


# ... the exception interface lists must execute after changing the
# default mode, which they will do as 'default' comes before 'interface'
# and 'no-interface'

class Cvt_RtrOSPF_PasvInt_Int(DiffConvert_RtrOSPF):
    cmd = "passive-interface",
    ext = "interface", None

    def delete(self, old, rem, new, proc, int_name):
        # if we're changing the default mode, the old list of exceptions
        # will be removed by that, so we don't need to do it
        if (old or {}).get("default") == (new or {}).get("default"):
            return self.enter(proc) + [" no passive-interface " + int_name]

    def update(self, old, upd, new, proc, int_name):
        return self.enter(proc) + [" passive-interface " + int_name]


class Cvt_RtrOSPF_PasvInt_NoInt(DiffConvert_RtrOSPF):
    cmd = "passive-interface",
    ext = "no-interface", None

    def delete(self, old, rem, new, proc, int_name):
        # if we're changing the default mode, the old list of exceptions
        # will be removed by that, so we don't need to do it
        if (old or {}).get("default") == (new or {}).get("default"):
            return self.enter(proc) + [" passive-interface " + int_name]

    def update(self, old, upd, new, proc, int_name):
        return self.enter(proc) + [" no passive-interface " + int_name]



# router ospfv3 ...



class Cvt_RtrOSPFv3(DiffConvert):
    cmd = "router", "ospfv3", None

    def remove(self, old, proc):
        return "no router ospfv3 " + str(proc)

    def add(self, new, proc):
        return "router ospfv3 " + str(proc)


class DiffConvert_RtrOSPFv3(DiffConvert):
    context = "router", "ospfv3", None

    def enter(self, proc):
        return ["router ospfv3 " + str(proc)]


class Cvt_RtrOSPFv3_Id(DiffConvert_RtrOSPFv3):
    cmd = "id",

    def remove(self, old, proc):
        return self.enter(proc) + [" no router-id"]

    def update(self, old, upd, new, proc):
        return self.enter(proc) + [" router-id " + new]


class Cvt_RtrOSPFv3_AreaNSSA(DiffConvert_RtrOSPFv3):
    cmd = "area", None, "nssa"

    def remove(self, old, proc, area):
        return self.enter(proc) + [" no area %s nssa" % area]

    def truncate(self, old, upd, new, proc, area):
        # if we're truncating, we're removing options and we do that by
        # just re-entering the command without them, same as update()
        return self.update(old, None, new, proc, area)

    def update(self, old, upd, new, proc, area):
        s = ""
        if "no-redistribution" in new: s += " no-redistribution"
        if "no-summary" in new: s += " no-summary"
        return self.enter(proc) + [" area %s nssa%s" % (area, s)]


class Cvt_RtrOSPFv3_AF(DiffConvert_RtrOSPFv3):
    cmd = "address-family", None

    def remove(self, old, vrf, af):
        return self.enter(vrf) + [" no address-family " + af]

    def add(self, new, vrf, af):
        return self.enter(vrf) + [" address-family " + af]


class DiffConvert_RtrOSPFv3_AF(DiffConvert_RtrOSPFv3):
    context = DiffConvert_RtrOSPFv3.context + Cvt_RtrOSPFv3_AF.cmd

    def enter(self, vrf, af):
        return super().enter(vrf) + [" address-family " + af]


# see the Cvt_RtrOSPF_... versions above for the explanation of how
# these converters work


class Cvt_RtrOSPFv3_AF_PasvInt_Dflt(DiffConvert_RtrOSPFv3_AF):
    cmd = "passive-interface", "default"

    def remove(self, old, proc, af):
        return self.enter(proc, af) + [" no passive-interface default"]

    def update(self, old, upd, new, proc, af):
        return self.enter(proc, af) + [" passive-interface default"]


class Cvt_RtrOSPFv3_AF_PasvInt_Int(DiffConvert_RtrOSPFv3_AF):
    cmd = "passive-interface",
    ext = "interface", None

    def delete(self, old, rem, new, proc, af, int_name):
        if (old or {}).get("default") == (new or {}).get("default"):
            return self.enter(proc, af) + [" no passive-interface " + int_name]

    def update(self, old, upd, new, proc, af, int_name):
        return self.enter(proc, af) + [" passive-interface " + int_name]


class Cvt_RtrOSPFv3_AF_PasvInt_NoInt(DiffConvert_RtrOSPFv3_AF):
    cmd = "passive-interface",
    ext = "no-interface", None

    def delete(self, old, rem, new, proc, af, int_name):
        if (old or {}).get("default") == (new or {}).get("default"):
            return self.enter(proc, af) + [" passive-interface " + int_name]

    def update(self, old, upd, new, proc, af, int_name):
        return self.enter(proc, af) + [" no passive-interface " + int_name]
