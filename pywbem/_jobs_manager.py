#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
"""
The :class:`~pywbem.WBEMJobsManager` class is a  manager for CIM Jobs
that provides for managing long running tasks defined by the DMTF CIM Jobs and
subclasses on multiple WBEM servers
"""
__all__ = ['WBEMSubscriptionManager']


class WBEMJobsManager(object):
    """
    A class for managing CIM Jobs on WBEM servers.

    The class may be used as a Python context manager, in order to get
    automatic clean up (see :meth:`~pywbem.WBEMSubscriptionManager.__exit__`).
    """

    def __init__(self, subscription_manager_id):
        """
        Parameters:
        """
        self._servers = {}  # WBEMServer objects for the WBEM servers

    def __repr__(self):
        """
        Return a representation of the :class:`~pywbem.WBEMJobsManager`
        object with all attributes, that is suitable for debugging.
        """
        return "%s(_subscription_manager_id=%r,)" % \
               (self.__class__.__name__,)

    def __enter__(self):
        """
        Enter method when the class is used as a context manager.
        Returns the subscription manager object
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit method when the class is used as a context manager.

        It cleans up by calling
        :meth:`~pywbem.WBEMSubscriptionManager.remove_all_servers`.
        """
        self.remove_all_servers()
        return False  # re-raise any exceptions

    def add_server(self, server):
    def add_server(self, server):
        """
        Register a WBEM server with the subscription manager. This is a
        prerequisite for adding listener destinations, indication filters and
        indication subscriptions to the server.

        This method discovers listener destination, indication filter, and
        subscription instances in the WBEM server that are owned by this
        subscription manager, and registers them in the subscription manager
        as if they had been created through it.

        In this discovery process, listener destination and indication filter
        instances are matched based upon the value of their `Name` property.
        Subscription instances are matched based upon the ownership of the
        referenced destination and filter instances: If a subscription
        references a filter or a destination that is owned by this subscription
        manager, it is considered owned by this subscription manager as well.

        Parameters:

          server (:class:`~pywbem.WBEMServer`):
            The WBEM server.

        Returns:

            :term:`string`: An ID for the WBEM server, for use by other
            methods of this class.

        Raises:

            Exceptions raised by :class:`~pywbem.WBEMConnection`.
            ValueError, TypeError for incorrect input parameters.
        """

        if not isinstance(server, WBEMServer):
            raise TypeError("Server argument of add_server() must be a "
                            "WBEMServer object")
        server_id = server.url
        if server_id in self._servers:
            raise ValueError("WBEM server already known by listener: %s" %
                             server_id)

        # Create dictionary entries for this server
        self._servers[server_id] = server
