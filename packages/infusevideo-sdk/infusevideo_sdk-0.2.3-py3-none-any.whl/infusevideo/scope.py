from .errors import InvalidScopeError


validScope = [
	"account_admin",
	"global_admin",
	"media:create",
	"media:delete",
	"media:list",
	"media:modify",
	"media:upload",
	"playlist:create",
	"playlist:delete",
	"playlist:list",
	"playlist:modify",
	"clip:list",
	"clip:create",
	"clip:modify",
	"clip:delete",
	"scene:list",
	"scene:create",
	"scene:modify",
	"scene:delete",
]
"""List of valid scope values for the API"""
# FIXME maybe dict with explanation. Can dump on the commandline? or just in a doc.

scopeGroups = {
	"all": [
		"read",
		"write",
		"admin",
	],
	"admin": [
		"account_admin",
	],
	"read": [
		"media:list",
		"playlist:list",
		"clip:list",
		"scene:list",
	],
	"writeNoDelete": [
		"read",
		"media:create",
		"media:modify",
		"media:upload",
		"playlist:create",
		"playlist:modify",
		"clip:create",
		"clip:modify",
		"scene:create",
		"scene:modify",
	],
	"write": [
		"writeNoDelete",
		"media:delete",
		"playlist:delete",
		"clip:delete",
		"scene:delete",
	],
}
"""The scopes, grouped in some convenience groups"""


def resolve_scope(scope: set[str]) -> set[str]:
	resolved = set()
	for s in scope:
		if s in scopeGroups:
			resolved |= resolve_scope(set(scopeGroups[s]))
		elif s in validScope:
			resolved.add(s)
		else:
			raise InvalidScopeError(s)
	return resolved
