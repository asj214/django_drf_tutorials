from rest_framework import permissions

'''
컨텐츠 본인 소유 혹은 슈퍼 어드민만 수정, 삭제가 가능하도록 하는 권한
'''


class IsOwnerOrReadOnly(permissions.BasePermission):
    # message = 'You Don\'t Have Permission!!'
    # message = {'errors': ['User is not a superuser']}
    message = {'errors': 'You Don\'t Have Permission!!'}
    

    def has_permission(slef, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(
            obj.user == request.user
            or request.user.level >= 900
        )