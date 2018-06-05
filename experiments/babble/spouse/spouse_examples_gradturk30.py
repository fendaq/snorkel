from snorkel.contrib.babble import Explanation

explanations = [
    Explanation(
        name='LF1',
        condition="person2 occurs in a phrase surrounded by quotes",
        candidate='2a339c82-5086-40e8-91ba-e705418acc0d::span:2635:2636~~2a339c82-5086-40e8-91ba-e705418acc0d::span:2668:2683',
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.and', ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2))))), ('.string', u'"')), ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 2))))), ('.string', u'"')))))
        ),

    Explanation(
        name='LF2',
        condition="the last word of person1 is not the same as the last word of person2.",
        candidate='445ee1bb-f00d-4fb6-a917-ad4609c37918::span:1714:1728~~445ee1bb-f00d-4fb6-a917-ad4609c37918::span:1756:1767',
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.neq', ('.index_word', ('.arg_to_string', ('.arg', ('.int', 2))), ('.int', -1))), ('.index_word', ('.arg_to_string', ('.arg', ('.int', 1))), ('.int', -1)))))
        ),

    Explanation(
        name='LF3',
        condition=""" "Beau Ryan's (Wife)" occurs before person1""",
        candidate='bd43aacf-2b13-40fa-bd9d-e08a3f26d89d::span:2055:2066~~bd43aacf-2b13-40fa-bd9d-e08a3f26d89d::span:2128:2136',
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 1))))), ('.string', u"Beau Ryan's (Wife)"))))
        ),

    Explanation(
        name='LF4',
        condition="The word 'rape' appears before person1 and the word 'trying' appears between person1 and person2",
        candidate='d38fa137-ac2d-4e43-b216-18dacf22426d::span:3814:3823~~d38fa137-ac2d-4e43-b216-18dacf22426d::span:3957:3970',
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.and', ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 1))))), ('.string', u'rape')), ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u'trying')))))
        ),

    Explanation(
        name='LF5',
        condition="person2 is the subject of the sentence and person1 is immediately preceded by 'husband'",
        candidate='affed66e-3a08-40d0-b11f-51b5727dccc4::span:61:64~~affed66e-3a08-40d0-b11f-51b5727dccc4::span:112:121',
        label=True,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.eq', ('.bool', True)), ('.bool', False)))) # NOTE: this is not the actual correct parse, but the specified condition is unrepresentable.
        ),
        # partial: semantics=('.root', ('.label', ('.bool', True), ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 1)), ('.string', '.eq'), ('.int', 1), ('.string', 'words')))), ('.string', u'husband'))))

    Explanation(
        name='LF6',
        condition="The words 'pictured together' appear between person1 and person2",
        candidate='c24931e6-be98-4056-ae2d-ab91fe5a2514::span:2054:2065~~c24931e6-be98-4056-ae2d-ab91fe5a2514::span:2087:2095',
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u'pictured together'))))
        ),

    Explanation(
        name='LF7',
        condition="'said' occurs between person1 and person2 and 'investigation' occurs after person2",
        candidate='75e1d890-c481-40fb-8d12-34fe6bcbd56d::span:4417:4422~~75e1d890-c481-40fb-8d12-34fe6bcbd56d::span:4446:4457',
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.and', ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u'said')), ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 2))))), ('.string', u'investigation')))))
        ),

    Explanation(
        name='LF8',
        condition="'scornful' appears after person1 and person2",
        candidate='63d7922b-ba07-47d2-88c1-06431c7302a9::span:3887:3901~~63d7922b-ba07-47d2-88c1-06431c7302a9::span:3927:3939',
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.composite_and_func', ('.list', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 1))))), ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 2))))))), ('.string', u'scornful'))))
        ),

    Explanation(
        name='LF9',
        condition="'husband' occurs before person2",
        candidate='a8488aab-31dc-49d7-83f0-8921c4bda307::span:0:15~~a8488aab-31dc-49d7-83f0-8921c4bda307::span:53:66',
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2))))), ('.string', u'husband'))))
        ),

    Explanation(
        name='LF10',
        condition="'executive director' is between person1 and person2",
        candidate='416228c4-81cb-4e38-8c4c-5ca61e385055::span:2721:2734~~416228c4-81cb-4e38-8c4c-5ca61e385055::span:2876:2886',
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u'executive director'))))
        ),

    Explanation(
        name='LF11',
        condition='person2 is an empty string.',
        candidate='7fc3e510-c4e6-44c2-a24b-f9a39bfcfb07::span:6956:6966~~7fc3e510-c4e6-44c2-a24b-f9a39bfcfb07::span:7134:7135',
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.eq', ('.string', u'  ')), ('.arg_to_string', ('.arg', ('.int', 2))))))
        ),

    Explanation(
        name='LF12',
        condition="the word 'Congress' appears four words before person2",
        candidate='c03ca255-1e1c-4031-93c0-623d91188e97::span:2237:2244~~c03ca255-1e1c-4031-93c0-623d91188e97::span:2420:2426',
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2)), ('.string', '.eq'), ('.int', 4), ('.string', 'words')))), ('.string', u'Congress'))))
        ),

    Explanation(
        name='LF13',
        condition="(person2 contains 'Osteen') and (person1 contains 1 token) and ('and' is between person1 and person2)",
        candidate='e7b41f2f-d98a-45a1-9616-1d4a65e24501::span:81:84~~e7b41f2f-d98a-45a1-9616-1d4a65e24501::span:90:104',
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.contains', ('.string', u'Osteen')), ('.arg_to_string', ('.arg', ('.int', 2)))), ('.and', ('.call', ('.eq', ('.index_word', ('.arg_to_string', ('.arg', ('.int', 1))), ('.int', -1))), ('.index_word', ('.arg_to_string', ('.arg', ('.int', 1))), ('.int', 1))), ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u'and'))))))
        ),

    Explanation(
        name='LF14',
        condition="the word 'hubby' is directly before person2",
        candidate='c4631b6d-747f-470d-a8ce-74b5b379cb86::span:1476:1484~~c4631b6d-747f-470d-a8ce-74b5b379cb86::span:1562:1568',
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2)), ('.string', '.eq'), ('.int', 1), ('.string', 'words')))), ('.string', u'hubby'))))
        ),

    Explanation(
        name='LF15',
        condition="'wife' precedes person2",
        candidate='d83554df-ec54-4ffc-a56d-f7145374dcdd::span:603:618~~d83554df-ec54-4ffc-a56d-f7145374dcdd::span:643:647',
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2))))), ('.string', u'wife'))))
        ),

    Explanation(
        name='LF16',
        condition="'wife' occurs between person1 and person2",
        candidate='8cf2a99f-ae08-4f65-b204-801de88cf1ec::span:359:367~~8cf2a99f-ae08-4f65-b204-801de88cf1ec::span:387:398',
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u'wife'))))
        ),

    Explanation(
        name='LF17',
        condition="'and' is between person1 and person2, and 'their son' comes less than 10 words after person1 and person2.",
        candidate='a8488aab-31dc-49d7-83f0-8921c4bda307::span:1084:1092~~a8488aab-31dc-49d7-83f0-8921c4bda307::span:1175:1188',
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u'and')), ('.call', ('.composite_and_func', ('.list', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 1)), ('.string', '.lt'), ('.int', 10), ('.string', 'words')))), ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 2)), ('.string', '.lt'), ('.int', 10), ('.string', 'words')))))), ('.string', u'their son')))))
        ),

    Explanation(
        name='LF18',
        condition='person1 and person2 are not people.',
        candidate='05ae8661-f643-4974-ab9b-93648737e1ad::span:2206:2215~~05ae8661-f643-4974-ab9b-93648737e1ad::span:2221:2233',
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.eq', ('.bool', True)), ('.bool', False)))) # NOTE: this is not the actual correct parse, but by definition, the system thinks both arg1 and arg2 are people, so this condition will never fire.
        ),

    Explanation(
        name='LF19',
        condition="person1 is the same as person2",
        candidate='77c632db-103a-491e-ae8c-cd7ef3aace00::span:14775:14779~~77c632db-103a-491e-ae8c-cd7ef3aace00::span:15046:15050',
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.eq', ('.arg_to_string', ('.arg', ('.int', 2)))), ('.arg_to_string', ('.arg', ('.int', 1))))))
        ),

    Explanation(
        name='LF20',
        condition="The word 'grandfather' appears one word to the left of person1",
        candidate='6c242461-04a2-4d76-89b7-ecf20995032f::span:572:593~~6c242461-04a2-4d76-89b7-ecf20995032f::span:751:761',
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 1)), ('.string', '.eq'), ('.int', 1), ('.string', 'words')))), ('.string', u'grandfather'))))
        ),

    Explanation(
        name='LF21',
        condition="'sister' comes immediately after person1, and 'sister' comes immediately before person2.",
        candidate='09cd2a7e-7963-45ea-8bf7-e58de8bbb363::span:6640:6649~~09cd2a7e-7963-45ea-8bf7-e58de8bbb363::span:6658:6662',
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.and', ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 1)), ('.string', '.eq'), ('.int', 1), ('.string', 'words')))), ('.string', u'sister')), ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 2)), ('.string', '.eq'), ('.int', 1), ('.string', 'words')))), ('.string', u'sister')))))
        ),

    Explanation(
        name='LF22',
        condition="person1 is said to be 'married' to person2 'from 1983 to 1988'",
        candidate='c24931e6-be98-4056-ae2d-ab91fe5a2514::span:2453:2461~~c24931e6-be98-4056-ae2d-ab91fe5a2514::span:2508:2518',
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u'married')), ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 2))))), ('.string', u'from 1983 to 1988'))))) # NOTE: This is my best guess at what they meant?
        ),

    Explanation(
        name='LF23',
        condition="because of the words 'and her husband' after person2.",
        candidate='a933e597-8f1f-4ccd-abdc-fadf12afaa88::span:978:981~~a933e597-8f1f-4ccd-abdc-fadf12afaa88::span:1018:1029',
        label=False,
        semantics=('.root', ('.label', ('.bool', False), ('.call', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 2))))), ('.string', u'and her husband'))))
        ),

    Explanation(
        name='LF24',
        condition="The word 'and' occurs between person1 and person2, and the words 'married couple' occur after person1 and person2.",
        candidate='e2657a53-566f-49d8-a6cf-8d676fd9c429::span:833:846~~e2657a53-566f-49d8-a6cf-8d676fd9c429::span:852:866',
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u'and')), ('.call', ('.composite_and_func', ('.list', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 1))))), ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 2))))))), ('.string', u'married couple')))))
        ),

    Explanation(
        name='LF25',
        condition="'husband' is in the sentence before person1",
        candidate='a8488aab-31dc-49d7-83f0-8921c4bda307::span:315:323~~a8488aab-31dc-49d7-83f0-8921c4bda307::span:329:342',
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.call', ('.in', ('.extract_text', ('.sentence',))), ('.string', u'husband'))))
        ),

    Explanation(
        name='LF26',
        condition="'wife' appears between person1 and person2 and the last word of person1 is the same as the last word of person2",
        candidate='c6a853a3-960e-4857-b048-abb692d1b2cc::span:1271:1280~~c6a853a3-960e-4857-b048-abb692d1b2cc::span:1469:1481',
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u'wife')), ('.call', ('.eq', ('.index_word', ('.arg_to_string', ('.arg', ('.int', 2))), ('.int', -1))), ('.index_word', ('.arg_to_string', ('.arg', ('.int', 1))), ('.int', -1))))))
        ),

    Explanation(
        name='LF27',
        condition="The words 'his marriage' and 'wife' occur between person1 and person2.",
        candidate='14112548-367a-4de1-85a7-11cd145b18e0::span:903:915~~14112548-367a-4de1-85a7-11cd145b18e0::span:1046:1059',
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.all', ('.map', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.list', ('.string', u'his marriage'), ('.string', u'wife'))))))
        ),

    Explanation(
        name='LF28',
        condition="'tied the knot' is between person1 and person2",
        candidate='258873e6-1f83-4f6c-9ddd-7e23b4332e41::span:319:324~~258873e6-1f83-4f6c-9ddd-7e23b4332e41::span:373:384',
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u'tied the knot'))))
        ),

    Explanation(
        name='LF29',
        condition="'and' is between person1 and person2, and 'proposal' follows (person1 and person2) in the sentence.",
        candidate='c9062ccc-f63b-4bd1-95e2-3d3ccc6391eb::span:2765:2768~~c9062ccc-f63b-4bd1-95e2-3d3ccc6391eb::span:2858:2862',
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.and', ('.call', ('.in', ('.extract_text', ('.between', ('.list', ('.arg', ('.int', 1)), ('.arg', ('.int', 2)))))), ('.string', u'and')), ('.call', ('.composite_and_func', ('.list', ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 1))))), ('.in', ('.extract_text', ('.right', ('.arg', ('.int', 2))))))), ('.string', u'proposal')))))
        ),

    Explanation(
        name='LF30',
        condition="'husband' occurs right before person1",
        candidate='de7b0df3-ed3a-4f5d-a53a-cd24d91240db::span:2600:2605~~de7b0df3-ed3a-4f5d-a53a-cd24d91240db::span:2608:2611',
        label=True,
        semantics=('.root', ('.label', ('.bool', True), ('.call', ('.in', ('.extract_text', ('.left', ('.arg', ('.int', 1)), ('.string', '.eq'), ('.int', 1), ('.string', 'words')))), ('.string', u'husband'))))
        ),
]

def get_explanations():
    return explanations