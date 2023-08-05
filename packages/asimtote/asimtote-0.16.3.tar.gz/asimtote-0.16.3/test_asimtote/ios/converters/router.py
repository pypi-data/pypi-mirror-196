# (asimtote) test_asimtote.ios.converters.router
#
# Copyright (C) Robert Franklin <rcf34@cam.ac.uk>



import unittest

from .cvtunittest import CiscoIOS_Convert_unittest



class TestAsimtote_CiscoIOS_Convert_Router(CiscoIOS_Convert_unittest):
    # =========================================================================
    # ip route ...
    # =========================================================================



    def test_IPRoute_add_int(self):
        self.old_cfg.parse_str("")

        self.new_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 Eth1/1.100
""")

        self.compare("""
ip route 10.0.0.0 255.255.255.0 Eth1/1.100
""")


    # -------------------------------------------------------------------------


    def test_IPRoute_add_ip(self):
        self.old_cfg.parse_str("")

        self.new_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 20.0.0.1
""")

        self.compare("""
ip route 10.0.0.0 255.255.255.0 20.0.0.1
""")


    # -------------------------------------------------------------------------


    def test_IPRoute_add_int_ip(self):
        self.old_cfg.parse_str("")

        self.new_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 Vlan100 20.0.0.1
""")

        self.compare("""
ip route 10.0.0.0 255.255.255.0 Vl100 20.0.0.1
""")


    # -------------------------------------------------------------------------


    def test_IPRoute_add_int_ip2(self):
        self.old_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 Vlan100 20.0.0.1
""")

        self.new_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 Vlan100 20.0.0.1
ip route 10.0.0.0 255.255.255.0 Vlan100 20.0.0.2
""")

        self.compare("""
ip route 10.0.0.0 255.255.255.0 Vl100 20.0.0.2
""")


    # -------------------------------------------------------------------------


    def test_IPRoute_add_metric(self):
        self.old_cfg.parse_str("")

        self.new_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 Vlan100 20.0.0.1 50
""")

        self.compare("""
ip route 10.0.0.0 255.255.255.0 Vl100 20.0.0.1 50
""")


    # -------------------------------------------------------------------------


    def test_IPRoute_add_tag(self):
        self.old_cfg.parse_str("")

        self.new_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 Vlan100 20.0.0.1 tag 50
""")

        self.compare("""
ip route 10.0.0.0 255.255.255.0 Vl100 20.0.0.1 tag 50
""")


    # -------------------------------------------------------------------------


    def test_IPRoute_add_full(self):
        self.old_cfg.parse_str("")

        self.new_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 Vlan100 20.0.0.1 200 tag 50
""")

        self.compare("""
ip route 10.0.0.0 255.255.255.0 Vl100 20.0.0.1 200 tag 50
""")


    # -------------------------------------------------------------------------


    def test_IPRoute_remove_ip(self):
        self.old_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 20.0.0.1
""")

        self.new_cfg.parse_str("""
""")

        self.compare("""
no ip route 10.0.0.0 255.255.255.0 20.0.0.1
""")


    # -------------------------------------------------------------------------


    def test_IPRoute_remove_int(self):
        self.old_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 Vlan100
""")

        self.new_cfg.parse_str("""
""")

        self.compare("""
no ip route 10.0.0.0 255.255.255.0 Vl100
""")


    # -------------------------------------------------------------------------


    def test_IPRoute_remove_int_ip(self):
        self.old_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 Vlan100 20.0.0.1
""")

        self.new_cfg.parse_str("""
""")

        self.compare("""
no ip route 10.0.0.0 255.255.255.0 Vl100 20.0.0.1
""")


    # -------------------------------------------------------------------------


    def test_IPRoute_remove_int_ip2(self):
        self.old_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 Vlan100 20.0.0.1
ip route 10.0.0.0 255.255.255.0 Vlan100 20.0.0.2
""")

        self.new_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 Vlan100 20.0.0.1
""")

        self.compare("""
no ip route 10.0.0.0 255.255.255.0 Vl100 20.0.0.2
""")


    # -------------------------------------------------------------------------


    def test_IPRoute_update_int(self):
        self.old_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 20.0.0.1
""")

        self.new_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 Vlan100 20.0.0.1
""")

        self.compare("""
no ip route 10.0.0.0 255.255.255.0 20.0.0.1
!
ip route 10.0.0.0 255.255.255.0 Vl100 20.0.0.1
""")


    # -------------------------------------------------------------------------


    def test_IPRoute_update_ip(self):
        self.old_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 Vlan100 20.0.0.1
""")

        self.new_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 Vlan100 20.0.0.2
""")

        self.compare("""
no ip route 10.0.0.0 255.255.255.0 Vl100 20.0.0.1
!
ip route 10.0.0.0 255.255.255.0 Vl100 20.0.0.2
""")


    # -------------------------------------------------------------------------


    def test_IPRoute_update_metric(self):
        self.old_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 Vlan100 20.0.0.1 50
""")

        self.new_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 Vlan100 20.0.0.1 60
""")

        self.compare("""
ip route 10.0.0.0 255.255.255.0 Vl100 20.0.0.1 60
""")


    # -------------------------------------------------------------------------


    def test_IPRoute_update_tag(self):
        self.old_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 Vlan100 20.0.0.1 tag 100
""")

        self.new_cfg.parse_str("""
ip route 10.0.0.0 255.255.255.0 Vlan100 20.0.0.1 tag 200
""")

        self.compare("""
ip route 10.0.0.0 255.255.255.0 Vl100 20.0.0.1 tag 200
""")


    # =========================================================================
    # ipv6 route ...
    # =========================================================================



    def test_IPv6Route_add_int(self):
        self.old_cfg.parse_str("")

        self.new_cfg.parse_str("""
ipv6 route 10::/64 Eth1/1.100
""")

        self.compare("""
ipv6 route 10::/64 Eth1/1.100
""")


    # -------------------------------------------------------------------------


    def test_IPv6Route_add_ip(self):
        self.old_cfg.parse_str("")

        self.new_cfg.parse_str("""
ipv6 route 10::/64 20::1
""")

        self.compare("""
ipv6 route 10::/64 20::1
""")


    # -------------------------------------------------------------------------


    def test_IPv6Route_add_int_ip(self):
        self.old_cfg.parse_str("")

        self.new_cfg.parse_str("""
ipv6 route 10::/64 Vlan100 20::1
""")

        self.compare("""
ipv6 route 10::/64 Vl100 20::1
""")


    # -------------------------------------------------------------------------


    def test_IPv6Route_add_int_ip2(self):
        self.old_cfg.parse_str("""
ipv6 route 10::/64 Vlan100 20::1
""")

        self.new_cfg.parse_str("""
ipv6 route 10::/64 Vlan100 20::1
ipv6 route 10::/64 Vlan100 20::2
""")

        self.compare("""
ipv6 route 10::/64 Vl100 20::2
""")


    # -------------------------------------------------------------------------


    def test_IPv6Route_add_metric(self):
        self.old_cfg.parse_str("")

        self.new_cfg.parse_str("""
ipv6 route 10::/64 Vlan100 20::1 50
""")

        self.compare("""
ipv6 route 10::/64 Vl100 20::1 50
""")


    # -------------------------------------------------------------------------


    def test_IPv6Route_add_tag(self):
        self.old_cfg.parse_str("")

        self.new_cfg.parse_str("""
ipv6 route 10::/64 Vlan100 20::1 tag 50
""")

        self.compare("""
ipv6 route 10::/64 Vl100 20::1 tag 50
""")


    # -------------------------------------------------------------------------


    def test_IPv6Route_add_full(self):
        self.old_cfg.parse_str("")

        self.new_cfg.parse_str("""
ipv6 route 10::/64 Vlan100 20::1 200 tag 50
""")

        self.compare("""
ipv6 route 10::/64 Vl100 20::1 200 tag 50
""")


    # -------------------------------------------------------------------------


    def test_IPv6Route_remove_ip(self):
        self.old_cfg.parse_str("""
ipv6 route 10::/64 20::1
""")

        self.new_cfg.parse_str("""
""")

        self.compare("""
no ipv6 route 10::/64 20::1
""")


    # -------------------------------------------------------------------------


    def test_IPv6Route_remove_int(self):
        self.old_cfg.parse_str("""
ipv6 route 10::/64 Vlan100
""")

        self.new_cfg.parse_str("""
""")

        self.compare("""
no ipv6 route 10::/64 Vl100
""")


    # -------------------------------------------------------------------------


    def test_IPv6Route_remove_int_ip(self):
        self.old_cfg.parse_str("""
ipv6 route 10::/64 Vlan100 20::1
""")

        self.new_cfg.parse_str("""
""")

        self.compare("""
no ipv6 route 10::/64 Vl100 20::1
""")


    # -------------------------------------------------------------------------


    def test_IPv6Route_remove_int_ip2(self):
        self.old_cfg.parse_str("""
ipv6 route 10::/64 Vlan100 20::1
ipv6 route 10::/64 Vlan100 20::2
""")

        self.new_cfg.parse_str("""
ipv6 route 10::/64 Vlan100 20::1
""")

        self.compare("""
no ipv6 route 10::/64 Vl100 20::2
""")


    # -------------------------------------------------------------------------


    def test_IPv6Route_update_int(self):
        self.old_cfg.parse_str("""
ipv6 route 10::/64 20::1
""")

        self.new_cfg.parse_str("""
ipv6 route 10::/64 Vlan100 20::1
""")

        self.compare("""
no ipv6 route 10::/64 20::1
!
ipv6 route 10::/64 Vl100 20::1
""")


    # -------------------------------------------------------------------------


    def test_IPv6Route_update_ip(self):
        self.old_cfg.parse_str("""
ipv6 route 10::/64 Vlan100 20::1
""")

        self.new_cfg.parse_str("""
ipv6 route 10::/64 Vlan100 20::2
""")

        self.compare("""
no ipv6 route 10::/64 Vl100 20::1
!
ipv6 route 10::/64 Vl100 20::2
""")


    # -------------------------------------------------------------------------


    def test_IPv6Route_update_metric(self):
        self.old_cfg.parse_str("""
ipv6 route 10::/64 Vlan100 20::1 50
""")

        self.new_cfg.parse_str("""
ipv6 route 10::/64 Vlan100 20::1 60
""")

        self.compare("""
ipv6 route 10::/64 Vl100 20::1 60
""")


    # -------------------------------------------------------------------------


    def test_IPv6Route_update_tag(self):
        self.old_cfg.parse_str("""
ipv6 route 10::/64 Vlan100 20::1 tag 100
""")

        self.new_cfg.parse_str("""
ipv6 route 10::/64 Vlan100 20::1 tag 200
""")

        self.compare("""
ipv6 route 10::/64 Vl100 20::1 tag 200
""")


    # =========================================================================
    # route-map ...
    # =========================================================================



    def test_RtMap_add_new(self):
        self.old_cfg.parse_str("")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
""")


    # -------------------------------------------------------------------------


    def test_RtMap_add__one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
!
route-map TestRouteMap deny 20
""")

        self.compare("""
route-map TestRouteMap deny 20
""")


    # -------------------------------------------------------------------------


    def test_RtMap_remove_all(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
!
route-map TestRouteMap deny 20
""")

        self.new_cfg.parse_str("")

        self.compare("""
no route-map TestRouteMap
""")


    # -------------------------------------------------------------------------


    def test_RtMap_remove_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
!
route-map TestRouteMap deny 20
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
no route-map TestRouteMap 20
""")


    # -------------------------------------------------------------------------


    def test_RtMap_update(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap deny 10
""")

        self.compare("""
route-map TestRouteMap deny 10
""")


    # =========================================================================
    # route-map ...
    #  match community ...
    # =========================================================================


    def test_RtMap_MatchCmty_add_first(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match community TestCommunityList
""")

        self.compare("""
route-map TestRouteMap permit 10
 match community TestCommunityList
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchCmty_add_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match community TestCommunityList1
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match community TestCommunityList1
 match community TestCommunityList2
""")

        self.compare("""
route-map TestRouteMap permit 10
 match community TestCommunityList2
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchCmty_add_multi(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match community TestCommunityList1
 match community TestCommunityList2
""")

        self.compare("""
route-map TestRouteMap permit 10
 match community TestCommunityList1
!
route-map TestRouteMap permit 10
 match community TestCommunityList2
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchCmty_remove_only(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match community TestCommunityList
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no match community TestCommunityList
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchCmty_remove_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match community TestCommunityList1
 match community TestCommunityList2
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match community TestCommunityList1
""")

        self.compare("""
route-map TestRouteMap permit 10
 no match community TestCommunityList2
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchCmty_remove_all(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match community TestCommunityList1
 match community TestCommunityList2
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no match community TestCommunityList1
!
route-map TestRouteMap permit 10
 no match community TestCommunityList2
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchCmty_update_exact_new(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match community TestCommunityList1
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match community TestCommunityList1
 match community TestCommunityList2 exact-match

""")

        self.compare("""
route-map TestRouteMap permit 10
 match community TestCommunityList2 exact-match
""")


    # -------------------------------------------------------------------------


    def TODO_test_RtMap_MatchCmty_update_exact_same(self):
        # TODO: this tests something that doesn't work yet (applying
        # 'exact-match' when the list stays the same)
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match community TestCommunityList
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match community TestCommunityList exact-match
""")

        self.compare("""
route-map TestRouteMap permit 10
 match community TestCommunityList exact-match
""")


    # =========================================================================
    # route-map ...
    #  match ip address ...
    # =========================================================================



    def test_RtMap_MatchIPAddr_add_first(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ip address TestACL
""")

        self.compare("""
route-map TestRouteMap permit 10
 match ip address TestACL
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPAddr_add_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ip address TestACL1
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ip address TestACL1
 match ip address TestACL2
""")

        self.compare("""
route-map TestRouteMap permit 10
 match ip address TestACL2
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPAddr_add_multi(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ip address TestACL1
 match ip address TestACL2
""")

        self.compare("""
route-map TestRouteMap permit 10
 match ip address TestACL1
 match ip address TestACL2
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPAddr_remove_only(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ip address TestACL
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no match ip address TestACL
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPAddr_remove_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ip address TestACL1
 match ip address TestACL2
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ip address TestACL1
""")

        self.compare("""
route-map TestRouteMap permit 10
 no match ip address TestACL2
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPAddr_remove_all(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ip address TestACL1
 match ip address TestACL2
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no match ip address TestACL1
 no match ip address TestACL2
""")


    # =========================================================================
    # route-map ...
    #  match ip address prefix-list ...
    # =========================================================================



    def test_RtMap_MatchIPPfxLst_add_first(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ip address prefix-list TestPrefixList
""")

        self.compare("""
route-map TestRouteMap permit 10
 match ip address prefix-list TestPrefixList
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPPfxLst_add_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ip address prefix-list TestPrefixList1
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ip address prefix-list TestPrefixList1
 match ip address prefix-list TestPrefixList2
""")

        self.compare("""
route-map TestRouteMap permit 10
 match ip address prefix-list TestPrefixList2
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPPfxLst_add_multi(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ip address prefix-list TestPrefixList1
 match ip address prefix-list TestPrefixList2
""")

        self.compare("""
route-map TestRouteMap permit 10
 match ip address prefix-list TestPrefixList1
 match ip address prefix-list TestPrefixList2
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPPfxLst_remove_only(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ip address prefix-list TestPrefixList
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no match ip address prefix-list TestPrefixList
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPPfxLst_remove_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ip address prefix-list TestPrefixList1
 match ip address prefix-list TestPrefixList2
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ip address prefix-list TestPrefixList1
""")

        self.compare("""
route-map TestRouteMap permit 10
 no match ip address prefix-list TestPrefixList2
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPPfxLst_remove_all(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ip address prefix-list TestPrefixList1
 match ip address prefix-list TestPrefixList2
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no match ip address prefix-list TestPrefixList1
 no match ip address prefix-list TestPrefixList2
""")


    # =========================================================================
    # route-map ...
    #  match ipv6 address ...
    # =========================================================================



    def test_RtMap_MatchIPv6Addr_add_first(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ipv6 address TestACL
""")

        self.compare("""
route-map TestRouteMap permit 10
 match ipv6 address TestACL
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPv6Addr_add_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ipv6 address TestACL1
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ipv6 address TestACL1
 match ipv6 address TestACL2
""")

        self.compare("""
route-map TestRouteMap permit 10
 match ipv6 address TestACL2
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPv6Addr_add_multi(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ipv6 address TestACL1
 match ipv6 address TestACL2
""")

        self.compare("""
route-map TestRouteMap permit 10
 match ipv6 address TestACL1
 match ipv6 address TestACL2
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPv6Addr_remove_only(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ipv6 address TestACL
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no match ipv6 address TestACL
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPv6Addr_remove_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ipv6 address TestACL1
 match ipv6 address TestACL2
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ipv6 address TestACL1
""")

        self.compare("""
route-map TestRouteMap permit 10
 no match ipv6 address TestACL2
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPv6Addr_remove_all(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ipv6 address TestACL1
 match ipv6 address TestACL2
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no match ipv6 address TestACL1
 no match ipv6 address TestACL2
""")


    # =========================================================================
    # route-map ...
    #  match ipv6 address prefix-list ...
    # =========================================================================



    def test_RtMap_MatchIPv6PfxLst_add_first(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ipv6 address prefix-list TestPrefixList
""")

        self.compare("""
route-map TestRouteMap permit 10
 match ipv6 address prefix-list TestPrefixList
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPv6PfxLst_add_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ipv6 address prefix-list TestPrefixList1
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ipv6 address prefix-list TestPrefixList1
 match ipv6 address prefix-list TestPrefixList2
""")

        self.compare("""
route-map TestRouteMap permit 10
 match ipv6 address prefix-list TestPrefixList2
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPv6PfxLst_add_multi(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ipv6 address prefix-list TestPrefixList1
 match ipv6 address prefix-list TestPrefixList2
""")

        self.compare("""
route-map TestRouteMap permit 10
 match ipv6 address prefix-list TestPrefixList1
 match ipv6 address prefix-list TestPrefixList2
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPv6PfxLst_remove_only(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ipv6 address prefix-list TestPrefixList
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no match ipv6 address prefix-list TestPrefixList
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPv6PfxLst_remove_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ipv6 address prefix-list TestPrefixList1
 match ipv6 address prefix-list TestPrefixList2
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ipv6 address prefix-list TestPrefixList1
""")

        self.compare("""
route-map TestRouteMap permit 10
 no match ipv6 address prefix-list TestPrefixList2
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchIPv6PfxLst_remove_all(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match ipv6 address prefix-list TestPrefixList1
 match ipv6 address prefix-list TestPrefixList2
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no match ipv6 address prefix-list TestPrefixList1
 no match ipv6 address prefix-list TestPrefixList2
""")


    # =========================================================================
    # route-map ...
    #  match tag ...
    # =========================================================================



    def test_RtMap_MatchTag_add_first(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match tag 100
""")

        self.compare("""
route-map TestRouteMap permit 10
 match tag 100
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchTag_add_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match tag 100
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match tag 100
 match tag 200
""")

        self.compare("""
route-map TestRouteMap permit 10
 match tag 200
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchTag_add_multi(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match tag 100
 match tag 200
""")

        self.compare("""
route-map TestRouteMap permit 10
 match tag 100
 match tag 200
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchTag_remove_only(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match tag 100
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no match tag 100
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchTag_remove_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match tag 100
 match tag 200
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 match tag 100
""")

        self.compare("""
route-map TestRouteMap permit 10
 no match tag 200
""")


    # -------------------------------------------------------------------------


    def test_RtMap_MatchTag_remove_all(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 match tag 100
 match tag 200
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no match tag 100
 no match tag 200
""")


    # =========================================================================
    # route-map ...
    #  set community ...
    # =========================================================================


    def test_RtMap_SetCmty_add_first(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set community 100:200
""")

        self.compare("""
route-map TestRouteMap permit 10
 set community 100:200
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetCmty_add_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set community 100:200
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set community 100:200 300:400
""")

        self.compare("""
route-map TestRouteMap permit 10
 set community 300:400
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetCmty_add_multi(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set community 100:200 300:400
""")

        self.compare("""
route-map TestRouteMap permit 10
 set community 100:200
 set community 300:400
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetCmty_remove_only(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set community 100:200
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set community 100:200
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetCmty_remove_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set community 100:200
 set community 300:400
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set community 100:200
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set community 300:400
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetCmty_remove_all(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set community 100:200
 set community 300:400
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set community 100:200
 no set community 300:400
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetCmty_update_additive_new(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set community 100:200
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set community 100:200
 set community 300:400 additive

""")

        self.compare("""
route-map TestRouteMap permit 10
 set community 300:400 additive
""")


    # -------------------------------------------------------------------------


    def TODO_test_RtMap_SetCmty_update_additive_same(self):
        # TODO: this tests something that doesn't work yet (applying
        # 'additive' when the list stays the same)
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set community 100:200
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set community 100:200 additive
""")

        self.compare("""
route-map TestRouteMap permit 10
 set community 100:200 additive
""")


    # -------------------------------------------------------------------------


    def TODO_test_RtMap_SetCmty_update_additive_remove(self):
        # TODO: this tests something that doesn't work yet (applying
        # 'additive' when the list stays the same)
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set community 100:200 additive
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set community 100:200
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set community
 set community 100:200
""")


    # =========================================================================
    # route-map ...
    #  set ip next-hop ...
    # =========================================================================


    # changing a list of next-hops clears the list and rebuilds it, in
    # case the order has changed (it might not have, and we're just
    # appending a new entry, but we don't know that)


    def test_RtMap_SetIPNxtHop_add_first(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop 10.0.0.1
""")

        self.compare("""
route-map TestRouteMap permit 10
 set ip next-hop 10.0.0.1
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetIPNxtHop_add_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop 10.0.0.1
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop 10.0.0.1
 set ip next-hop 20.0.0.1
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set ip next-hop 10.0.0.1
 set ip next-hop 10.0.0.1
 set ip next-hop 20.0.0.1
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetIPNxtHop_add_multi(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop 10.0.0.1
 set ip next-hop 20.0.0.1
""")

        self.compare("""
route-map TestRouteMap permit 10
 set ip next-hop 10.0.0.1
 set ip next-hop 20.0.0.1
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetIPNxtHop_remove_only(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop 10.0.0.1
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set ip next-hop 10.0.0.1
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetIPNxtHop_remove_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop 10.0.0.1 20.0.0.1
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop 10.0.0.1
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set ip next-hop 10.0.0.1
 no set ip next-hop 20.0.0.1
 set ip next-hop 10.0.0.1
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetIPNxtHop_remove_all(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop 10.0.0.1 20.0.0.1
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set ip next-hop 10.0.0.1
 no set ip next-hop 20.0.0.1
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetIPNxtHop_update_order(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop 10.0.0.1 20.0.0.1
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop 20.0.0.1
 set ip next-hop 10.0.0.1
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set ip next-hop 10.0.0.1
 no set ip next-hop 20.0.0.1
 set ip next-hop 20.0.0.1
 set ip next-hop 10.0.0.1
""")


    # =========================================================================
    # route-map ...
    #  set ip next-hop verify-availability
    # =========================================================================


    def test_RtMap_SetIPNxtHopVrfy_add(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop verify-availability
""")

        self.compare("""
route-map TestRouteMap permit 10
 set ip next-hop verify-availability
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetIPNxtHopVrfy_remove(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop verify-availability
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set ip next-hop verify-availability
""")


    # =========================================================================
    # route-map ...
    #  set ip next-hop verify-availability ...
    # =========================================================================


    def test_RtMap_SetIPNxtHopVrfyTrk_add_first(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop verify-availability 10.0.0.1 10 track 100
""")

        self.compare("""
route-map TestRouteMap permit 10
 set ip next-hop verify-availability 10.0.0.1 10 track 100
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetIPNxtHopVrfyTrk_add_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop verify-availability 10.0.0.1 10 track 100
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop verify-availability 10.0.0.1 10 track 100
 set ip next-hop verify-availability 20.0.0.1 20 track 100
""")

        self.compare("""
route-map TestRouteMap permit 10
 set ip next-hop verify-availability 20.0.0.1 20 track 100
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetIPNxtHopVrfyTrk_add_multi(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop verify-availability 10.0.0.1 10 track 100
 set ip next-hop verify-availability 20.0.0.1 20 track 100
""")

        self.compare("""
route-map TestRouteMap permit 10
 set ip next-hop verify-availability 10.0.0.1 10 track 100
!
route-map TestRouteMap permit 10
 set ip next-hop verify-availability 20.0.0.1 20 track 100
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetIPNxtHopVrfyTrk_add_order(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop verify-availability 20.0.0.1 20 track 100
 set ip next-hop verify-availability 10.0.0.1 10 track 100
""")

        self.compare("""
route-map TestRouteMap permit 10
 set ip next-hop verify-availability 10.0.0.1 10 track 100
!
route-map TestRouteMap permit 10
 set ip next-hop verify-availability 20.0.0.1 20 track 100
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetIPNxtHopVrfyTrk_remove_only(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop verify-availability 10.0.0.1 10 track 100
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set ip next-hop verify-availability 10.0.0.1 10 track 100
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetIPNxtHopVrfyTrk_remove_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop verify-availability 10.0.0.1 10 track 100
 set ip next-hop verify-availability 20.0.0.1 20 track 100
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop verify-availability 10.0.0.1 10 track 100
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set ip next-hop verify-availability 20.0.0.1 20 track 100
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetIPNxtHopVrfyTrk_remove_multi(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ip next-hop verify-availability 10.0.0.1 10 track 100
 set ip next-hop verify-availability 20.0.0.1 20 track 100
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set ip next-hop verify-availability 10.0.0.1 10 track 100
!
route-map TestRouteMap permit 10
 no set ip next-hop verify-availability 20.0.0.1 20 track 100
""")


    # =========================================================================
    # route-map ...
    #  set ipv6 next-hop ...
    # =========================================================================


    # changing a list of next-hops clears the list and rebuilds it, in
    # case the order has changed (it might not have, and we're just
    # appending a new entry, but we don't know that)


    def test_RtMap_SetIPv6NxtHop_add_first(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ipv6 next-hop 10::1
""")

        self.compare("""
route-map TestRouteMap permit 10
 set ipv6 next-hop 10::1
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetIPv6NxtHop_add_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ipv6 next-hop 10::1
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ipv6 next-hop 10::1
 set ipv6 next-hop 20::1
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set ipv6 next-hop 10::1
 set ipv6 next-hop 10::1
 set ipv6 next-hop 20::1
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetIPv6NxtHop_add_multi(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ipv6 next-hop 10::1
 set ipv6 next-hop 20::1
""")

        self.compare("""
route-map TestRouteMap permit 10
 set ipv6 next-hop 10::1
 set ipv6 next-hop 20::1
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetIPv6NxtHop_remove_only(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ipv6 next-hop 10::1
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set ipv6 next-hop 10::1
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetIPv6NxtHop_remove_one(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ipv6 next-hop 10::1 20::1
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ipv6 next-hop 10::1
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set ipv6 next-hop 10::1
 no set ipv6 next-hop 20::1
 set ipv6 next-hop 10::1
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetIPv6NxtHop_remove_all(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ipv6 next-hop 10::1 20::1
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set ipv6 next-hop 10::1
 no set ipv6 next-hop 20::1
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetIPv6NxtHop_update_order(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ipv6 next-hop 10::1 20::1
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set ipv6 next-hop 20::1
 set ipv6 next-hop 10::1
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set ipv6 next-hop 10::1
 no set ipv6 next-hop 20::1
 set ipv6 next-hop 20::1
 set ipv6 next-hop 10::1
""")


    # =========================================================================
    # route-map ...
    #  set local-preference ...
    # =========================================================================


    def test_RtMap_SetLocalPref_add(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set local-preference 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 set local-preference 10
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetLocalPref_remove(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set local-preference 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set local-preference
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetLocalPref_update(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set local-preference 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set local-preference 20
""")

        self.compare("""
route-map TestRouteMap permit 10
 set local-preference 20
""")


    # =========================================================================
    # route-map ...
    #  set {global,vrf} ...
    # =========================================================================


    def test_RtMap_SetVRF_add_global(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set global
""")

        self.compare("""
route-map TestRouteMap permit 10
 set global
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetVRF_add_vrf(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set vrf TestVRF
""")

        self.compare("""
route-map TestRouteMap permit 10
 set vrf TestVRF
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetVRF_remove_global(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set global
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set global
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetVRF_remove_vrf(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set vrf TestVRF
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set vrf TestVRF
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetVRF_update_vrf(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set vrf TestVRF1
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set vrf TestVRF2
""")

        self.compare("""
route-map TestRouteMap permit 10
 set vrf TestVRF2
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetVRF_update_global_vrf(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set global
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set vrf TestVRF
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set global
 set vrf TestVRF
""")


    # -------------------------------------------------------------------------


    def test_RtMap_SetVRF_update_vrf_global(self):
        self.old_cfg.parse_str("""
route-map TestRouteMap permit 10
 set vrf TestVRF
""")

        self.new_cfg.parse_str("""
route-map TestRouteMap permit 10
 set global
""")

        self.compare("""
route-map TestRouteMap permit 10
 no set vrf TestVRF
 set global
""")


    # =========================================================================
    # router ospf ...
    # =========================================================================


    def test_RtrOSPF_add(self):
        self.old_cfg.parse_str("")

        self.new_cfg.parse_str("""
router ospf 10
""")

        self.compare("""
router ospf 10
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPF_remove(self):
        self.old_cfg.parse_str("""
router ospf 10
""")

        self.new_cfg.parse_str("")

        self.compare("""
no router ospf 10
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPF_update(self):
        self.old_cfg.parse_str("""
router ospf 10
""")

        self.new_cfg.parse_str("""
router ospf 20
""")

        self.compare("""
no router ospf 10
!
router ospf 20
""")


    # =========================================================================
    # router ospf ...
    #  router-id ...
    # =========================================================================


    def test_RtrOSPF_Id_add(self):
        self.old_cfg.parse_str("""
router ospf 10
""")

        self.new_cfg.parse_str("""
router ospf 10
 router-id 10.0.0.1
""")

        self.compare("""
router ospf 10
 router-id 10.0.0.1
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPF_Id_remove(self):
        self.old_cfg.parse_str("""
router ospf 10
 router-id 10.0.0.1
""")

        self.new_cfg.parse_str("""
router ospf 10
""")

        self.compare("""
router ospf 10
 no router-id
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPF_Id_update(self):
        self.old_cfg.parse_str("""
router ospf 10
 router-id 10.0.0.1
""")

        self.new_cfg.parse_str("""
router ospf 10
 router-id 20.0.0.1
""")

        self.compare("""
router ospf 10
 router-id 20.0.0.1
""")


    # =========================================================================
    # router ospf ...
    #  area ... nssa
    # =========================================================================


    def test_RtrOSPF_AreaNSSA_add(self):
        self.old_cfg.parse_str("""
router ospf 10
""")

        self.new_cfg.parse_str("""
router ospf 10
 area 10.0.0.0 nssa
""")

        self.compare("""
router ospf 10
 area 10.0.0.0 nssa
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPF_AreaNSSA_remove(self):
        self.old_cfg.parse_str("""
router ospf 10
 area 10.0.0.0 nssa
""")

        self.new_cfg.parse_str("""
router ospf 10
""")

        self.compare("""
router ospf 10
 no area 10.0.0.0 nssa
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPF_AreaNSSA_update_no_opts(self):
        self.old_cfg.parse_str("""
router ospf 10
 area 10.0.0.0 nssa no-redistribution no-summary
""")

        self.new_cfg.parse_str("""
router ospf 10
 area 10.0.0.0 nssa
""")

        self.compare("""
router ospf 10
 area 10.0.0.0 nssa
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPF_AreaNSSA_update_opts(self):
        self.old_cfg.parse_str("""
router ospf 10
 area 10.0.0.0 nssa
""")

        self.new_cfg.parse_str("""
router ospf 10
 area 10.0.0.0 nssa no-redistribution no-summary
""")

        self.compare("""
router ospf 10
 area 10.0.0.0 nssa no-redistribution no-summary
""")


    # =========================================================================
    # router ospf ...
    #  [no] passive-interface default
    # =========================================================================


    def test_RtrOSPF_PasvInt_Dflt_add(self):
        self.old_cfg.parse_str("""
router ospf 10
""")

        self.new_cfg.parse_str("""
router ospf 10
 passive-interface default
""")

        self.compare("""
router ospf 10
 passive-interface default
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPF_PasvInt_Dflt_remove(self):
        self.old_cfg.parse_str("""
router ospf 10
 passive-interface default
""")

        self.new_cfg.parse_str("""
router ospf 10
""")

        self.compare("""
router ospf 10
 no passive-interface default
""")


    # =========================================================================
    # router ospf ...
    #  passive-interface ...
    # =========================================================================


    def test_RtrOSPF_PasvInt_Int_add_pasv(self):
        self.old_cfg.parse_str("""
router ospf 10
""")

        self.new_cfg.parse_str("""
router ospf 10
 passive-interface Eth1/1
""")

        self.compare("""
router ospf 10
 passive-interface Eth1/1
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPF_PasvInt_Int_add_no_pasv(self):
        self.old_cfg.parse_str("""
router ospf 10
 passive-interface default
""")

        self.new_cfg.parse_str("""
router ospf 10
 passive-interface default
 no passive-interface Eth1/1
""")

        self.compare("""
router ospf 10
 no passive-interface Eth1/1
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPF_PasvInt_Int_remove_pasv(self):
        self.old_cfg.parse_str("""
router ospf 10
 passive-interface Eth1/1
""")

        self.new_cfg.parse_str("""
router ospf 10
""")

        self.compare("""
router ospf 10
 no passive-interface Eth1/1
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPF_PasvInt_Int_remove_no_pasv(self):
        self.old_cfg.parse_str("""
router ospf 10
 passive-interface default
 no passive-interface Eth1/1
""")

        self.new_cfg.parse_str("""
router ospf 10
 passive-interface default
""")

        self.compare("""
router ospf 10
 passive-interface Eth1/1
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPF_PasvInt_Int_update_to_pasv(self):
        self.old_cfg.parse_str("""
router ospf 10
 passive-interface Eth1/1
""")

        self.new_cfg.parse_str("""
router ospf 10
 passive-interface default
 no passive-interface Eth2/1
""")

        self.compare("""
router ospf 10
 passive-interface default
!
router ospf 10
 no passive-interface Eth2/1
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPF_PasvInt_Int_update_to_no_pasv(self):
        self.old_cfg.parse_str("""
router ospf 10
 passive-interface default
 no passive-interface Eth1/1
""")

        self.new_cfg.parse_str("""
router ospf 10
 passive-interface Eth2/1
""")

        self.compare("""
router ospf 10
 no passive-interface default
!
router ospf 10
 passive-interface Eth2/1
""")


    # =========================================================================
    # router ospfv3 ...
    # =========================================================================


    def test_RtrOSPF_add(self):
        self.old_cfg.parse_str("")

        self.new_cfg.parse_str("""
router ospfv3 10
""")

        self.compare("""
router ospfv3 10
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPF_remove(self):
        self.old_cfg.parse_str("""
router ospfv3 10
""")

        self.new_cfg.parse_str("")

        self.compare("""
no router ospfv3 10
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPF_update(self):
        self.old_cfg.parse_str("""
router ospfv3 10
""")

        self.new_cfg.parse_str("""
router ospfv3 20
""")

        self.compare("""
no router ospfv3 10
!
router ospfv3 20
""")


    # =========================================================================
    # router ospfv3 ...
    #  router-id ...
    # =========================================================================


    def test_RtrOSPFv3_Id_add(self):
        self.old_cfg.parse_str("""
router ospfv3 10
""")

        self.new_cfg.parse_str("""
router ospfv3 10
 router-id 10.0.0.1
""")

        self.compare("""
router ospfv3 10
 router-id 10.0.0.1
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPFv3_Id_remove(self):
        self.old_cfg.parse_str("""
router ospfv3 10
 router-id 10.0.0.1
""")

        self.new_cfg.parse_str("""
router ospfv3 10
""")

        self.compare("""
router ospfv3 10
 no router-id
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPFv3_Id_update(self):
        self.old_cfg.parse_str("""
router ospfv3 10
 router-id 10.0.0.1
""")

        self.new_cfg.parse_str("""
router ospfv3 10
 router-id 20.0.0.1
""")

        self.compare("""
router ospfv3 10
 router-id 20.0.0.1
""")


    # =========================================================================
    # router ospfv3 ...
    #  area ... nssa
    # =========================================================================


    def test_RtrOSPFv3_AreaNSSA_add(self):
        self.old_cfg.parse_str("""
router ospfv3 10
""")

        self.new_cfg.parse_str("""
router ospfv3 10
 area 10.0.0.0 nssa
""")

        self.compare("""
router ospfv3 10
 area 10.0.0.0 nssa
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPFv3_AreaNSSA_remove(self):
        self.old_cfg.parse_str("""
router ospfv3 10
 area 10.0.0.0 nssa
""")

        self.new_cfg.parse_str("""
router ospfv3 10
""")

        self.compare("""
router ospfv3 10
 no area 10.0.0.0 nssa
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPFv3_AreaNSSA_update_no_opts(self):
        self.old_cfg.parse_str("""
router ospfv3 10
 area 10.0.0.0 nssa no-redistribution no-summary
""")

        self.new_cfg.parse_str("""
router ospfv3 10
 area 10.0.0.0 nssa
""")

        self.compare("""
router ospfv3 10
 area 10.0.0.0 nssa
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPFv3_AreaNSSA_update_opts(self):
        self.old_cfg.parse_str("""
router ospfv3 10
 area 10.0.0.0 nssa
""")

        self.new_cfg.parse_str("""
router ospfv3 10
 area 10.0.0.0 nssa no-redistribution no-summary
""")

        self.compare("""
router ospfv3 10
 area 10.0.0.0 nssa no-redistribution no-summary
""")


    # =========================================================================
    # router ospfv3 ...
    #  address-family ...
    # =========================================================================


    def test_RtrOSPFv3_AF_add_plain(self):
        self.old_cfg.parse_str("""
router ospfv3 10
""")

        self.new_cfg.parse_str("""
router ospfv3 10
 address-family ipv4
""")

        self.compare("""
router ospfv3 10
 address-family ipv4
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPFv3_AF_add_unicast(self):
        # check 'unicast' is effectively ignored

        self.old_cfg.parse_str("""
router ospfv3 10
""")

        self.new_cfg.parse_str("""
router ospfv3 10
 address-family ipv4 unicast
""")

        self.compare("""
router ospfv3 10
 address-family ipv4
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPFv3_AF_add_multi(self):
        # check 'unicast' is effectively ignored

        self.old_cfg.parse_str("""
router ospfv3 10
""")

        self.new_cfg.parse_str("""
router ospfv3 10
 address-family ipv4
 exit-address-family
 !
 address-family ipv6
 exit-address-family
""")

        self.compare("""
router ospfv3 10
 address-family ipv4
!
router ospfv3 10
 address-family ipv6
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPFv3_AF_remove(self):
        self.old_cfg.parse_str("""
router ospfv3 10
 address-family ipv4
""")

        self.new_cfg.parse_str("""
router ospfv3 10
""")

        self.compare("""
router ospfv3 10
 no address-family ipv4
""")


    # =========================================================================
    # router ospfv3 ...
    #  address-family ...
    #   [no] passive-interface default
    # =========================================================================


    def test_RtrOSPFv3_AF_PasvInt_Dflt_add(self):
        self.old_cfg.parse_str("""
router ospfv3 10
 address-family ipv4
""")

        self.new_cfg.parse_str("""
router ospfv3 10
 address-family ipv4
  passive-interface default
""")

        self.compare("""
router ospfv3 10
 address-family ipv4
  passive-interface default
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPFv3_AF_PasvInt_Dflt_remove(self):
        self.old_cfg.parse_str("""
router ospfv3 10
 address-family ipv4
  passive-interface default
""")

        self.new_cfg.parse_str("""
router ospfv3 10
 address-family ipv4
""")

        self.compare("""
router ospfv3 10
 address-family ipv4
  no passive-interface default
""")


    # =========================================================================
    # router ospfv3 ...
    #  address-family ...
    #   passive-interface ...
    # =========================================================================


    def test_RtrOSPFv3_AF_PasvInt_Int_add_pasv(self):
        self.old_cfg.parse_str("""
router ospfv3 10
 address-family ipv4
""")

        self.new_cfg.parse_str("""
router ospfv3 10
 address-family ipv4
  passive-interface Eth1/1
""")

        self.compare("""
router ospfv3 10
 address-family ipv4
  passive-interface Eth1/1
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPFv3_AF_PasvInt_Int_add_no_pasv(self):
        self.old_cfg.parse_str("""
router ospfv3 10
 address-family ipv4
  passive-interface default
""")

        self.new_cfg.parse_str("""
router ospfv3 10
 address-family ipv4
  passive-interface default
  no passive-interface Eth1/1
""")

        self.compare("""
router ospfv3 10
 address-family ipv4
  no passive-interface Eth1/1
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPFv3_AF_PasvInt_Int_remove_pasv(self):
        self.old_cfg.parse_str("""
router ospfv3 10
 address-family ipv4
  passive-interface Eth1/1
""")

        self.new_cfg.parse_str("""
router ospfv3 10
 address-family ipv4
""")

        self.compare("""
router ospfv3 10
 address-family ipv4
  no passive-interface Eth1/1
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPFv3_AF_PasvInt_Int_remove_no_pasv(self):
        self.old_cfg.parse_str("""
router ospfv3 10
 address-family ipv4
  passive-interface default
  no passive-interface Eth1/1
""")

        self.new_cfg.parse_str("""
router ospfv3 10
 address-family ipv4
  passive-interface default
""")

        self.compare("""
router ospfv3 10
 address-family ipv4
  passive-interface Eth1/1
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPFv3_AF_PasvInt_Int_update_to_pasv(self):
        self.old_cfg.parse_str("""
router ospfv3 10
 address-family ipv4
  passive-interface Eth1/1
""")

        self.new_cfg.parse_str("""
router ospfv3 10
 address-family ipv4
  passive-interface default
  no passive-interface Eth2/1
""")

        self.compare("""
router ospfv3 10
 address-family ipv4
  passive-interface default
!
router ospfv3 10
 address-family ipv4
  no passive-interface Eth2/1
""")


    # -------------------------------------------------------------------------


    def test_RtrOSPFv3_AF_PasvInt_Int_update_to_no_pasv(self):
        self.old_cfg.parse_str("""
router ospfv3 10
 address-family ipv4
  passive-interface default
  no passive-interface Eth1/1
""")

        self.new_cfg.parse_str("""
router ospfv3 10
 address-family ipv4
  passive-interface Eth2/1
""")

        self.compare("""
router ospfv3 10
 address-family ipv4
  no passive-interface default
!
router ospfv3 10
 address-family ipv4
  passive-interface Eth2/1
""")
