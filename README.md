# examples

Play from console:

```console
$ npm test PI
$ npm test RZ2
$ npm test BigPHI
```

Other "radix values" available are:
```
export const VALS = {
    BigPHI: Decimal.sqrt(5).plus(1).div(2),
    // note the rest of these have no been converted to Decimal size (maybe you can?)
    C1: Math.log(Math.PI**2),
    C2: Math.log(Math.PI**2) - Math.log(6) + 1, /* not sum of 1 and reciprocals of squares of primes */
    C3: 1.4522474200410654985065, /* correct C2 */
    HBARC: 3.16152649, /* plankc in radians */
    EM1: 1.57721566490153286060651209008240243, /* Euler M constant */
    RZ2: Math.PI**2/6,
    PISOTV3: 1.4432687912703731076,
    PISOTV6: 1.5341577449142669154,
    PISOTV9: 1.5701473121960543629,
    FIB_PSI: 3.35988566624317755317201130291892,
    PSI: 1.465571231876768026656731,
    APERY: 1.2020569031595942853997381,
    P: 1.32471795724474602596,
    PI: Math.PI,
    SQRT2: Math.SQRT2,              /* no OEIS */
    PHI: 0.5+Math.sqrt(5)/2,        /* golden mean, as binary is A336231 */
    "2PHI": 2/(0.5+Math.sqrt(5)/2), /* 2-inverse of golden mean, no OEIS */
    DELTA: 1+Math.SQRT2,            /* silver mean */
    BRONZE: (3+Math.sqrt(13))/2,    /* bronze mean */
    SQRT3: Math.sqrt(3),
    SQRT3IPHI: Math.sqrt(3+1/(0.5+Math.sqrt(5)/2)),
    E: Math.E,
    G: Math.E**Math.PI,
    G20: Math.E**Math.PI-Math.PI,
    G20T: (Math.E**Math.PI-Math.PI)/10
  };
  VALS.P2 = VALS.P**2;
```

Some test.js output:

```js
// integer packing
{
  X: [ 1942769, 2, 115410, 98, 32659001 ],
  packed: Uint32Array(5) [ 151636467, 129840031, 2223618, 136283967, 412 ],
  unpacked: [ 1942769, 2, 115410, 98, 32659001 ]
}

// irrational base conversion (e.g base BigPHI)
{ baseI: '0', back: 0, i: 0 }
{ baseI: '1', back: 1, i: 1 }
{ baseI: '10', back: 2, i: 2 }
{ baseI: '11', back: 3, i: 3 }
{ baseI: '100', back: 4, i: 4 }
{ baseI: '110', back: 5, i: 5 }
{ baseI: '111', back: 6, i: 6 }
{ baseI: '1000', back: 7, i: 7 }
{ baseI: '1001', back: 8, i: 8 }
{ baseI: '1100', back: 9, i: 9 }
{ baseI: '1110', back: 10, i: 10 }
{ baseI: '1111', back: 11, i: 11 }
{ baseI: '10000', back: 12, i: 12 }
{ baseI: '10010', back: 13, i: 13 }
{ baseI: '10011', back: 14, i: 14 }
{ baseI: '11000', back: 15, i: 15 }
{ baseI: '11001', back: 16, i: 16 }
{ baseI: '11100', back: 17, i: 17 }
{ baseI: '11110', back: 18, i: 18 }
{ baseI: '11111', back: 19, i: 19 }
{ baseI: '100000', back: 20, i: 20 }
{ baseI: '100001', back: 21, i: 21 }
{ baseI: '100100', back: 22, i: 22 }
{ baseI: '100110', back: 23, i: 23 }
{ baseI: '100111', back: 24, i: 24 }
{ baseI: '110000', back: 25, i: 25 }
{ baseI: '110010', back: 26, i: 26 }
{ baseI: '110011', back: 27, i: 27 }
{ baseI: '111000', back: 28, i: 28 }
{ baseI: '111001', back: 29, i: 29 }
{ baseI: '111100', back: 30, i: 30 }
{ baseI: '111110', back: 31, i: 31 }
{ baseI: '111111', back: 32, i: 32 }
{ baseI: '1000000', back: 33, i: 33 }
{ baseI: '1000010', back: 34, i: 34 }
{ baseI: '1000011', back: 35, i: 35 }
{ baseI: '1001000', back: 36, i: 36 }
{ baseI: '1001001', back: 37, i: 37 }
{ baseI: '1001100', back: 38, i: 38 }
{ baseI: '1001110', back: 39, i: 39 }
{ baseI: '1001111', back: 40, i: 40 }
{ baseI: '1100000', back: 41, i: 41 }
{ baseI: '1100001', back: 42, i: 42 }
{ baseI: '1100100', back: 43, i: 43 }
{ baseI: '1100110', back: 44, i: 44 }
{ baseI: '1100111', back: 45, i: 45 }
{ baseI: '1110000', back: 46, i: 46 }
{ baseI: '1110010', back: 47, i: 47 }
{ baseI: '1110011', back: 48, i: 48 }
{ baseI: '1111000', back: 49, i: 49 }
{ baseI: '1111001', back: 50, i: 50 }
{ baseI: '1111100', back: 51, i: 51 }
{ baseI: '1111110', back: 52, i: 52 }
{ baseI: '1111111', back: 53, i: 53 }
{ baseI: '10000000', back: 54, i: 54 }
{ baseI: '10000001', back: 55, i: 55 }
{ baseI: '10000100', back: 56, i: 56 }
{ baseI: '10000110', back: 57, i: 57 }
{ baseI: '10000111', back: 58, i: 58 }
{ baseI: '10010000', back: 59, i: 59 }
{ baseI: '10010010', back: 60, i: 60 }
{ baseI: '10010011', back: 61, i: 61 }
{ baseI: '10011000', back: 62, i: 62 }
{ baseI: '10011001', back: 63, i: 63 }
{ baseI: '10011100', back: 64, i: 64 }

// more (base BigPHI)
{ based: '1001000000100', back: 666, i: 666 }
{ based: '1001000000110', back: 667, i: 667 }
{ based: '1001000000111', back: 668, i: 668 }
{ based: '1001000010000', back: 669, i: 669 }
{ based: '1001000010010', back: 670, i: 670 }
{ based: '1001000010011', back: 671, i: 671 }
{ based: '1001000011000', back: 672, i: 672 }
{ based: '1001000011001', back: 673, i: 673 }
{ based: '1001000011100', back: 674, i: 674 }
{ based: '1001000011110', back: 675, i: 675 }
{ based: '1001000011111', back: 676, i: 676 }
{ based: '1001001000000', back: 677, i: 677 }
{ based: '1001001000010', back: 678, i: 678 }
{ based: '1001001000011', back: 679, i: 679 }
{ based: '1001001001000', back: 680, i: 680 }
{ based: '1001001001001', back: 681, i: 681 }
{ based: '1001001001100', back: 682, i: 682 }
{ based: '1001001001110', back: 683, i: 683 }
{ based: '1001001001111', back: 684, i: 684 }
{ based: '1001001100000', back: 685, i: 685 }
{ based: '1001001100001', back: 686, i: 686 }
{ based: '1001001100100', back: 687, i: 687 }
{ based: '1001001100110', back: 688, i: 688 }
{ based: '1001001100111', back: 689, i: 689 }
{ based: '1001001110000', back: 690, i: 690 }
{ based: '1001001110010', back: 691, i: 691 }
{ based: '1001001110011', back: 692, i: 692 }
{ based: '1001001111000', back: 693, i: 693 }
{ based: '1001001111001', back: 694, i: 694 }
{ based: '1001001111100', back: 695, i: 695 }
{ based: '1001001111110', back: 696, i: 696 }
{ based: '1001001111111', back: 697, i: 697 }
{ based: '1001100000000', back: 698, i: 698 }
{ based: '1001100000010', back: 699, i: 699 }
{ based: '1001100000011', back: 700, i: 700 }
{ based: '1001100001000', back: 701, i: 701 }
{ based: '1001100001001', back: 702, i: 702 }
{ based: '1001100001100', back: 703, i: 703 }
{ based: '1001100001110', back: 704, i: 704 }
{ based: '1001100001111', back: 705, i: 705 }
{ based: '1001100100000', back: 706, i: 706 }
{ based: '1001100100001', back: 707, i: 707 }
{ based: '1001100100100', back: 708, i: 708 }
{ based: '1001100100110', back: 709, i: 709 }
{ based: '1001100100111', back: 710, i: 710 }
{ based: '1001100110000', back: 711, i: 711 }
{ based: '1001100110010', back: 712, i: 712 }
{ based: '1001100110011', back: 713, i: 713 }
{ based: '1001100111000', back: 714, i: 714 }
{ based: '1001100111001', back: 715, i: 715 }
{ based: '1001100111100', back: 716, i: 716 }
{ based: '1001100111110', back: 717, i: 717 }
{ based: '1001100111111', back: 718, i: 718 }
{ based: '1001110000000', back: 719, i: 719 }
{ based: '1001110000001', back: 720, i: 720 }
{ based: '1001110000100', back: 721, i: 721 }
{ based: '1001110000110', back: 722, i: 722 }
{ based: '1001110000111', back: 723, i: 723 }
{ based: '1001110010000', back: 724, i: 724 }
{ based: '1001110010010', back: 725, i: 725 }
{ based: '1001110010011', back: 726, i: 726 }
{ based: '1001110011000', back: 727, i: 727 }
{ based: '1001110011001', back: 728, i: 728 }
{ based: '1001110011100', back: 729, i: 729 }
{ based: '1001110011110', back: 730, i: 730 }
{ based: '1001110011111', back: 731, i: 731 }
{ based: '1001111000000', back: 732, i: 732 }
{ based: '1001111000010', back: 733, i: 733 }
{ based: '1001111000011', back: 734, i: 734 }
{ based: '1001111001000', back: 735, i: 735 }
{ based: '1001111001001', back: 736, i: 736 }
{ based: '1001111001100', back: 737, i: 737 }
{ based: '1001111001110', back: 738, i: 738 }
{ based: '1001111001111', back: 739, i: 739 }
{ based: '1001111100000', back: 740, i: 740 }
{ based: '1001111100001', back: 741, i: 741 }
{ based: '1001111100100', back: 742, i: 742 }
{ based: '1001111100110', back: 743, i: 743 }
{ based: '1001111100111', back: 744, i: 744 }
{ based: '1001111110000', back: 745, i: 745 }
{ based: '1001111110010', back: 746, i: 746 }
{ based: '1001111110011', back: 747, i: 747 }
{ based: '1001111111000', back: 748, i: 748 }
{ based: '1001111111001', back: 749, i: 749 }
{ based: '1001111111100', back: 750, i: 750 }
{ based: '1001111111110', back: 751, i: 751 }
{ based: '1001111111111', back: 752, i: 752 }
{ based: '1100000000000', back: 753, i: 753 }
{ based: '1100000000001', back: 754, i: 754 }
{ based: '1100000000100', back: 755, i: 755 }
{ based: '1100000000110', back: 756, i: 756 }
{ based: '1100000000111', back: 757, i: 757 }
{ based: '1100000010000', back: 758, i: 758 }
{ based: '1100000010010', back: 759, i: 759 }
{ based: '1100000010011', back: 760, i: 760 }
{ based: '1100000011000', back: 761, i: 761 }
{ based: '1100000011001', back: 762, i: 762 }
{ based: '1100000011100', back: 763, i: 763 }
{ based: '1100000011110', back: 764, i: 764 }
{ based: '1100000011111', back: 765, i: 765 }
{ based: '1100001000000', back: 766, i: 766 }
{ based: '1100001000010', back: 767, i: 767 }
{ based: '1100001000011', back: 768, i: 768 }
{ based: '1100001001000', back: 769, i: 769 }
{ based: '1100001001001', back: 770, i: 770 }
{ based: '1100001001100', back: 771, i: 771 }
{ based: '1100001001110', back: 772, i: 772 }
{ based: '1100001001111', back: 773, i: 773 }
{ based: '1100001100000', back: 774, i: 774 }
{ based: '1100001100001', back: 775, i: 775 }
{ based: '1100001100100', back: 776, i: 776 }
{ based: '1100001100110', back: 777, i: 777 }
{ based: '1100001100111', back: 778, i: 778 }
{ based: '1100001110000', back: 779, i: 779 }
{ based: '1100001110010', back: 780, i: 780 }
{ based: '1100001110011', back: 781, i: 781 }
{ based: '1100001111000', back: 782, i: 782 }
{ based: '1100001111001', back: 783, i: 783 }
{ based: '1100001111100', back: 784, i: 784 }
{ based: '1100001111110', back: 785, i: 785 }
{ based: '1100001111111', back: 786, i: 786 }
{ based: '1100100000000', back: 787, i: 787 }
{ based: '1100100000010', back: 788, i: 788 }
{ based: '1100100000011', back: 789, i: 789 }
{ based: '1100100001000', back: 790, i: 790 }
{ based: '1100100001001', back: 791, i: 791 }
{ based: '1100100001100', back: 792, i: 792 }
{ based: '1100100001110', back: 793, i: 793 }
{ based: '1100100001111', back: 794, i: 794 }
{ based: '1100100100000', back: 795, i: 795 }
{ based: '1100100100001', back: 796, i: 796 }
{ based: '1100100100100', back: 797, i: 797 }
{ based: '1100100100110', back: 798, i: 798 }
{ based: '1100100100111', back: 799, i: 799 }
{ based: '1100100110000', back: 800, i: 800 }
{ based: '1100100110010', back: 801, i: 801 }
{ based: '1100100110011', back: 802, i: 802 }
{ based: '1100100111000', back: 803, i: 803 }
{ based: '1100100111001', back: 804, i: 804 }
{ based: '1100100111100', back: 805, i: 805 }
{ based: '1100100111110', back: 806, i: 806 }
{ based: '1100100111111', back: 807, i: 807 }
{ based: '1100110000000', back: 808, i: 808 }
{ based: '1100110000001', back: 809, i: 809 }
{ based: '1100110000100', back: 810, i: 810 }
{ based: '1100110000110', back: 811, i: 811 }
{ based: '1100110000111', back: 812, i: 812 }
{ based: '1100110010000', back: 813, i: 813 }
{ based: '1100110010010', back: 814, i: 814 }
{ based: '1100110010011', back: 815, i: 815 }
{ based: '1100110011000', back: 816, i: 816 }
{ based: '1100110011001', back: 817, i: 817 }
{ based: '1100110011100', back: 818, i: 818 }
{ based: '1100110011110', back: 819, i: 819 }
{ based: '1100110011111', back: 820, i: 820 }
{ based: '1100111000000', back: 821, i: 821 }
{ based: '1100111000010', back: 822, i: 822 }
{ based: '1100111000011', back: 823, i: 823 }
{ based: '1100111001000', back: 824, i: 824 }
{ based: '1100111001001', back: 825, i: 825 }
{ based: '1100111001100', back: 826, i: 826 }
{ based: '1100111001110', back: 827, i: 827 }
{ based: '1100111001111', back: 828, i: 828 }
{ based: '1100111100000', back: 829, i: 829 }
{ based: '1100111100001', back: 830, i: 830 }
{ based: '1100111100100', back: 831, i: 831 }
{ based: '1100111100110', back: 832, i: 832 }
{ based: '1100111100111', back: 833, i: 833 }
{ based: '1100111110000', back: 834, i: 834 }
{ based: '1100111110010', back: 835, i: 835 }
{ based: '1100111110011', back: 836, i: 836 }
{ based: '1100111111000', back: 837, i: 837 }
{ based: '1100111111001', back: 838, i: 838 }
{ based: '1100111111100', back: 839, i: 839 }
{ based: '1100111111110', back: 840, i: 840 }
{ based: '1100111111111', back: 841, i: 841 }
{ based: '1110000000000', back: 842, i: 842 }
{ based: '1110000000010', back: 843, i: 843 }
{ based: '1110000000011', back: 844, i: 844 }
{ based: '1110000001000', back: 845, i: 845 }
{ based: '1110000001001', back: 846, i: 846 }
{ based: '1110000001100', back: 847, i: 847 }
{ based: '1110000001110', back: 848, i: 848 }
{ based: '1110000001111', back: 849, i: 849 }
{ based: '1110000100000', back: 850, i: 850 }
{ based: '1110000100001', back: 851, i: 851 }
{ based: '1110000100100', back: 852, i: 852 }
{ based: '1110000100110', back: 853, i: 853 }
{ based: '1110000100111', back: 854, i: 854 }
{ based: '1110000110000', back: 855, i: 855 }
{ based: '1110000110010', back: 856, i: 856 }
{ based: '1110000110011', back: 857, i: 857 }
{ based: '1110000111000', back: 858, i: 858 }
{ based: '1110000111001', back: 859, i: 859 }
{ based: '1110000111100', back: 860, i: 860 }
{ based: '1110000111110', back: 861, i: 861 }
{ based: '1110000111111', back: 862, i: 862 }
{ based: '1110010000000', back: 863, i: 863 }
{ based: '1110010000001', back: 864, i: 864 }
{ based: '1110010000100', back: 865, i: 865 }
{ based: '1110010000110', back: 866, i: 866 }
{ based: '1110010000111', back: 867, i: 867 }
{ based: '1110010010000', back: 868, i: 868 }
{ based: '1110010010010', back: 869, i: 869 }
{ based: '1110010010011', back: 870, i: 870 }
{ based: '1110010011000', back: 871, i: 871 }
{ based: '1110010011001', back: 872, i: 872 }
{ based: '1110010011100', back: 873, i: 873 }
{ based: '1110010011110', back: 874, i: 874 }
{ based: '1110010011111', back: 875, i: 875 }
{ based: '1110011000000', back: 876, i: 876 }
{ based: '1110011000010', back: 877, i: 877 }
{ based: '1110011000011', back: 878, i: 878 }
{ based: '1110011001000', back: 879, i: 879 }
{ based: '1110011001001', back: 880, i: 880 }
{ based: '1110011001100', back: 881, i: 881 }
{ based: '1110011001110', back: 882, i: 882 }
{ based: '1110011001111', back: 883, i: 883 }
{ based: '1110011100000', back: 884, i: 884 }
{ based: '1110011100001', back: 885, i: 885 }
{ based: '1110011100100', back: 886, i: 886 }
{ based: '1110011100110', back: 887, i: 887 }
{ based: '1110011100111', back: 888, i: 888 }
{ based: '1110011110000', back: 889, i: 889 }
{ based: '1110011110010', back: 890, i: 890 }
{ based: '1110011110011', back: 891, i: 891 }
{ based: '1110011111000', back: 892, i: 892 }
{ based: '1110011111001', back: 893, i: 893 }
{ based: '1110011111100', back: 894, i: 894 }
{ based: '1110011111110', back: 895, i: 895 }
{ based: '1110011111111', back: 896, i: 896 }
{ based: '1111000000000', back: 897, i: 897 }
{ based: '1111000000001', back: 898, i: 898 }
{ based: '1111000000100', back: 899, i: 899 }
{ based: '1111000000110', back: 900, i: 900 }
{ based: '1111000000111', back: 901, i: 901 }
{ based: '1111000010000', back: 902, i: 902 }
{ based: '1111000010010', back: 903, i: 903 }
{ based: '1111000010011', back: 904, i: 904 }
{ based: '1111000011000', back: 905, i: 905 }
{ based: '1111000011001', back: 906, i: 906 }
{ based: '1111000011100', back: 907, i: 907 }
{ based: '1111000011110', back: 908, i: 908 }
{ based: '1111000011111', back: 909, i: 909 }
{ based: '1111001000000', back: 910, i: 910 }
{ based: '1111001000010', back: 911, i: 911 }
{ based: '1111001000011', back: 912, i: 912 }
{ based: '1111001001000', back: 913, i: 913 }
{ based: '1111001001001', back: 914, i: 914 }
{ based: '1111001001100', back: 915, i: 915 }
{ based: '1111001001110', back: 916, i: 916 }
{ based: '1111001001111', back: 917, i: 917 }
{ based: '1111001100000', back: 918, i: 918 }
{ based: '1111001100001', back: 919, i: 919 }
{ based: '1111001100100', back: 920, i: 920 }
{ based: '1111001100110', back: 921, i: 921 }
{ based: '1111001100111', back: 922, i: 922 }
{ based: '1111001110000', back: 923, i: 923 }
{ based: '1111001110010', back: 924, i: 924 }
{ based: '1111001110011', back: 925, i: 925 }
{ based: '1111001111000', back: 926, i: 926 }
{ based: '1111001111001', back: 927, i: 927 }
{ based: '1111001111100', back: 928, i: 928 }
{ based: '1111001111110', back: 929, i: 929 }
{ based: '1111001111111', back: 930, i: 930 }
{ based: '1111100000000', back: 931, i: 931 }
{ based: '1111100000010', back: 932, i: 932 }
{ based: '1111100000011', back: 933, i: 933 }
{ based: '1111100001000', back: 934, i: 934 }
{ based: '1111100001001', back: 935, i: 935 }
{ based: '1111100001100', back: 936, i: 936 }
{ based: '1111100001110', back: 937, i: 937 }
{ based: '1111100001111', back: 938, i: 938 }
{ based: '1111100100000', back: 939, i: 939 }
{ based: '1111100100001', back: 940, i: 940 }
{ based: '1111100100100', back: 941, i: 941 }
{ based: '1111100100110', back: 942, i: 942 }
{ based: '1111100100111', back: 943, i: 943 }
{ based: '1111100110000', back: 944, i: 944 }
{ based: '1111100110010', back: 945, i: 945 }
{ based: '1111100110011', back: 946, i: 946 }
{ based: '1111100111000', back: 947, i: 947 }
{ based: '1111100111001', back: 948, i: 948 }
{ based: '1111100111100', back: 949, i: 949 }
{ based: '1111100111110', back: 950, i: 950 }
{ based: '1111100111111', back: 951, i: 951 }
{ based: '1111110000000', back: 952, i: 952 }
{ based: '1111110000001', back: 953, i: 953 }
{ based: '1111110000100', back: 954, i: 954 }
{ based: '1111110000110', back: 955, i: 955 }
{ based: '1111110000111', back: 956, i: 956 }
{ based: '1111110010000', back: 957, i: 957 }
{ based: '1111110010010', back: 958, i: 958 }
{ based: '1111110010011', back: 959, i: 959 }
{ based: '1111110011000', back: 960, i: 960 }
{ based: '1111110011001', back: 961, i: 961 }
{ based: '1111110011100', back: 962, i: 962 }
{ based: '1111110011110', back: 963, i: 963 }
{ based: '1111110011111', back: 964, i: 964 }
{ based: '1111111000000', back: 965, i: 965 }
{ based: '1111111000010', back: 966, i: 966 }
{ based: '1111111000011', back: 967, i: 967 }
{ based: '1111111001000', back: 968, i: 968 }
{ based: '1111111001001', back: 969, i: 969 }
{ based: '1111111001100', back: 970, i: 970 }
{ based: '1111111001110', back: 971, i: 971 }
{ based: '1111111001111', back: 972, i: 972 }
{ based: '1111111100000', back: 973, i: 973 }
{ based: '1111111100001', back: 974, i: 974 }
{ based: '1111111100100', back: 975, i: 975 }
{ based: '1111111100110', back: 976, i: 976 }
{ based: '1111111100111', back: 977, i: 977 }
{ based: '1111111110000', back: 978, i: 978 }
{ based: '1111111110010', back: 979, i: 979 }
{ based: '1111111110011', back: 980, i: 980 }
{ based: '1111111111000', back: 981, i: 981 }
{ based: '1111111111001', back: 982, i: 982 }
{ based: '1111111111100', back: 983, i: 983 }
{ based: '1111111111110', back: 984, i: 984 }
{ based: '1111111111111', back: 985, i: 985 }
{ based: '10000000000000', back: 986, i: 986 }
{ based: '10000000000001', back: 987, i: 987 }
{ based: '10000000000100', back: 988, i: 988 }
{ based: '10000000000110', back: 989, i: 989 }
{ based: '10000000000111', back: 990, i: 990 }
{ based: '10000000010000', back: 991, i: 991 }
{ based: '10000000010010', back: 992, i: 992 }
{ based: '10000000010011', back: 993, i: 993 }
{ based: '10000000011000', back: 994, i: 994 }
{ based: '10000000011001', back: 995, i: 995 }
{ based: '10000000011100', back: 996, i: 996 }
{ based: '10000000011110', back: 997, i: 997 }
{ based: '10000000011111', back: 998, i: 998 }
{ based: '10000001000000', back: 999, i: 999 }
```

```
# irradix

Irrational radices and integer packing into the Golden Ratio base. 

Did you know 1000 in base *e* is `2010102`? Now you do.

Did you also know that base phi (Golden Ratio) creates binary representations that have no "101" sequence?

At least, that's the hypothesis: Every sequence of 0 bits between any two 1 bits is always even-numbered. I discovered this fact while writing this library, and I realized it could be used to pack integers into a contiguous bit sequence (and then say, "chop" it up into discrete x-bit sized chunks). This packing, like the radix encoding, is reversible. I put the numbers I was getting into [OEIS](http://oeis.org/), and found this sequence](http://oeis.org/A336231), then supposed it was true for every integer, and tests up to some high values (million) then randomly tested multiple times across the space in 0 -- 2**53 (JS integer range). There might be a counter example somewhere!

# Math

Sorry this is not a proof, more of a discussion of my intuition about this. I only acquired this intutiont after noticing the fact, not before. Before creating this irrational radix, I had no idea, the golden ratio base would behave in this way. After investigation a range of other irrational radices, I noticed no other patterns (but surely there must be some). 

I think the "only even zero sequence between 1s" property of base PHI is related to the fact that phi represents a ratio of ratios, as in a:b ~ b:a+b, and because phi**2 = phi + 1, and any sequence of zeroes in the base-phi representation will correspond to an sequence of multiplications via phi, but phi**3 (or any odd-sequence of multiplications) will not have this identity. 

But that's about as far as I got. It would be great to see a proof of this, I think it should be pretty simple.

# Background

I experimented with this and found that for certain source number size distributions related to the chunks size (for example for x bit sized numbers, with x <=32 and for chunks up to 32 bit (matching regular JS type arrary sized slots)), this packing saves some space compared to the naive JS storage of 8 bytes per integer. 

This packing is not rocket science, nor do I think it's any special nor "highly compressed" bit packing. It's logical you should be able to save space when the naive slot is 8 bytes, but your integers only occupy a range of less than that. 

# Hypothesis

Because phi is involved, and because the packing is so simple, I have a feeling that this packing will (in the limit) approach some Shannon entropy limit relative to these distributions. In addition I don't think it's any sort of "fast converging" or "highly efficient" packing, but I do think it might be "among the simplest" sorts of packings of integers. 

Note that by "packing" I don't mean "compressing" an individual bit sequence, I only mean, joining numbers together into a continuous bit sequence while maintaining the boundary ('101') information for each individual number.

# Limitations

There is no support for "negative" numbers, but concievably you could add your own encoding for that (such as adding MAX_NEG_RANGE to all integers prior to packing).

There is no support (neither in the bit packing encoding, nor in the irrational radix representations) for non-integer numbers (only, non integer, even irrational radices).

# Development history

I started out using native JS number implementations. This was incredible fast (coding and packing millions of numbers in a second or two on an average VPS core), but I noticed that some numbers were not reverting to their originals on de-radificiation, and the packing was often broken. I surmised there were probably multiple issues, but that precision  could be one of them. I investigated and found the "non-revertible" numbers were those with long (~20 and above) sequences of zeroes (equating to long sequences of multiplication by phi), which seemed to indicate to me that precision was an issue, as errors would be compounded in these long sequences of multiplications. The precision of phi in JS was limited to the precision of the regular number types which (as is commonly known) have some precision issues relating to floating point.

So I then endeavoured (after I break) to reimplement this in a suitable "BigDecimal" library for JS, to allow arbitrary precision calculations. 

Once I did that, I discovered there were no more issues in the radifications. Hooray!

But there were still issues in the encodings (packings). I discovered a simple arithmetic issue in the encodings and fixed it, leading to fault free implementation. Yeah, I'm awesome! :p ;) xx

## Usage

```js
import {irradix, derradix, VALS, encode, decode} from 'irradix';

const rep = irradix('234232142312342342314213123321', VALS.BigPHI);
const num = derradix(rep, VALS.BigPHI);

const {packed,bits} = encode([123,3,54,45782348,48,1231,0,23]);
const unpacked = decode(packed, bits);
```

## `Decimal` return type

`derradix` returns a Decimal type. You need to call `.toFixed()` on that to get a string value of the base 10 representation. For more `Decimal` APIs [see its documentation](http://mikemcl.github.io/decimal.js/#toFixed)

## `bits` parameter

For encoding you can pass a bits parameters, which gives your indeded chunk size. 
But if you have a number which has a contiguous sequence of zeroes in its base-phi rep, and that bits size you passed in is smaller than what would be required to cut that number into a decodable chunk (not losing leading zeroes), then we will pass back a bits value indicating the number bit size of chunks actually created.

## Supports

- Any radix (above 10, units represented as a-z, above 36, representation has units separted by commas)
- Any irrational radix (PI, E, PHI, Math.sqrt(163), etc), also regular radices (like 4, or 9991)
- Negative radix
- Negative integers

## Does not support

- Radices of 1 or smaller
- Encoding non-integers
- BigInts (sorry, you can't mix BigInt and regular Numbers and so there's not much point, since BigInts can't be fractional)

## Why?

I had the idea. I thought it was cool. Nuff said. 

## ~But I like more detail...please explain~ But I like to know more so I can find something to criticize because I love telling people how wrong I think they are

OK, I literally just had the idea pop into my head. I went searching about it and found a couple of web pages saying "there are problems" using irratonal radixes, suggesting it was impossible. Or coming up with bizarre schemes that did not look radix-like to me (such as purely positional notation without powers, similar to the "Fibonacci" or "Prime" radix). 

I checked out the Wikipedia page, and honestly did not really understand it, and thought there has got to be a better way to do irrational (or fractional) radices. I basically understand what they do now, but I dislike it. I think there's a better representation. To my mind, the radix in an integer base is like this:

```math

N = kb + r

N - integer
k - divisor
r - remainder
b - base

So N can be written has a multiple of b plus the remainder.

Now, iterate with k.

k = k_2b + r_2

And so on, as every number can be written like this.

You end up with a polynomial in b

N = b^j.r_j + b^(j-1).r_{j-1} + ... + b.r_1 + r_0

Which is represented as a "numeral" by its coefficients (r_j..r_0)

```

And the "algorithm" for radix conversion (in the arrogant langauge of math papers) "emerges immediately" from the equation: you subtract remainders, and divide through by b, and repeat.

But it seems Wikipedia is talking about something different with irrational radices, that has the appearance (to me) of p-adic numbers. I don't know why they don't simply use the above remainder based representation. They say the scheme "reduces to regular integer" radix schemes when integer bases are used, but I don't see it. It seems like they are finding "bracketing powers" around an integer, and outputting I don't know what, and it seems like they ignore the remainder completely.  I don't know how to use their scheme, and I don't like their scheme. If I really wanted to understand it I would go back to the original papers they quote from the 50s, and read them. Original (and old) papers are usually pretty clear. 

Anyway, I'm pretty sure it's different to my (simpler) scheme, because the representations they quote are different to the ones I get. My "key insight" was that you can simply convert the irrational remainders you get to an integer that represents, how many integers past the product you need to go to your number.

So for example, if you divide 100 by PI you get a remainder of about 2.6

Which means that if you have something that you multiply by PI, then go up to the next integer (ceil) then 2 more (floor of the remainder), you get back to your number. So the "radix units" can simply be the floor values of the irrational remainders, and you can reconstruct your integers. And you can do that for every step in the algorithm. 

I was pretty happy to have a scheme where I can take any integer and convert it to any irrational base, and I get a sequence of "radix units" (called "digits" in base 10), that show how to represent that integer in that base. I just think that's pretty cool. 

Basically a radix is just representing a polynomial equation that shows the relationship between some number, and some base. I like that now you can get polynomial equations in some irrational number that show the relationship between that irrational and some integer. 

And "hiding the complexity" by reducing the irrational remainders to simple integers, that "stand in for" that coefficient being the rth integer above the product you are constructing, is a nice step.

I just think it's cool to have a sequence of units like that, that shows the relationship between an integer, and something so unwieldy as an irrational number.

## Caveats

- Obviously this is only good up to the precision you are calculating with. So Math.PI is not really PI it is just a representation of PI up to some number of bits. If JS had BigDecimals and constants that on-the-fly computed their bits to the required precision for any calculation, then I would be confident in saying that this scheme could really convert any integer, whatever the size, to any irrational number base, and be totally accurate. But if you push the integers high enough, probably two inaccuracies will happen: 1) the rep will differ from the "true rep" for that base, because you escaped the precision of the constant for that irrational, and 2) the rep might actually not be convertible back because you escape the precision of the numeric calculations. Those are both fairly "general" caveats, but worth mentioning for anything to do with numerical methods. 
- This scheme might be wrong in some way and have some overlooked corner cases. I've tried to cover the ones important to me (+ve and -ve integer magnitudes, and +ve and -ve real radices), but I've only tested up to 20,000 or so, and while that probably means it's solid, it might not be. Something erroneous could have slipped through.

## Get it

```console
npm i --save irradix
```

## Other interesting stuff

I conjecture this thing might be universal isomorphism over integer bit sequences, and sequences of integers, in the sense that, any bit sequence you can pass in can represent two things: either itself, or its "unpacked" "seqeunce of integers" self, and similarly any "sequence of integers" can represent either itself, or its "compressed" packed into a single bit sequence self. 

I like this. That there is a symmetry across these things, and it's particularly satisfying that it involves phi, the Golden Ratio. However, this may not be the case! It has not been proven and it still might turn out this thing is "not universal". But if so , the structure of those gappy regions might be interesting. 

## Contributions

I'm not a mathematician, this is just a hobby investigation for me, so I would really love if some people good at maths want to contribute some more cool maths stuff on this like proofs, or some way to get nice math formulae into the README. I would love that! So please join in if this interests you. Perhaps we can joint publish a paper on this "Golden Ratio base" (I have not seen anything referring to this in the literature).
